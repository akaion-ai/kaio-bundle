#!/usr/bin/env python3
"""Bundle Kaio per i siti: un comando mette tutto quello che si può mettere da solo.

    python3 bundle_install.py <cartella sito> <slug Kaio> [--no-chat] [--type BeautySalon]

Riconosce da solo il tipo di sito:
  - TanStack Start  (src/routes/__root.tsx, vite + nitro: i siti usciti da Lovable)
  - Next.js         (app/layout.tsx o src/app/layout.tsx)
  - HTML statico    (index.html nella cartella o in public/)

e ci mette:
  1. k.js        visite senza cookie (la «Presenza online» del negoziante)
  2. kchat.js    chat Kaio sul sito (salta con --no-chat)
  3. GEO         /llms.txt che risponde con i dati vivi di Kaio + scheda JSON-LD nel <head>
                 (serve che lo slug sia nella directory pubblica di Kaio)
  4. font locali niente Google Fonts dal browser (legal/fonts_local.py)

Poi controlla quello che non si può fare da soli e lo stampa come «DA FARE»:
resti di Lovable, /privacy e footer (servono i dati veri del titolare), noindex,
dominio in allowed_origins. Si può rilanciare: quello che c'è già resta com'è.
Poi commit, push, deploy. Solo libreria standard, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

API = "https://api.prod.akaion.com/api/service1/api/v1/kaio"
CDN = "https://smallbusiness.akaion.com"
HERE = Path(__file__).parent
# Specialità/settore Kaio → tipo schema.org. Il resto è LocalBusiness.
TYPES = {
    "Estetista": "BeautySalon", "Unghie": "NailSalon", "Parrucchiere": "HairSalon", "Barbiere": "HairSalon",
    "Terapeuta / massaggi e benessere": "DaySpa", "Fisioterapista": "Physiotherapy",
    "Palestra / personal trainer": "ExerciseGym", "Yoga e pilates": "SportsActivityLocation",
    "Edilizia": "GeneralContractor", "Studio medico": "MedicalClinic", "Ristorante / hotel": "FoodEstablishment",
    "Pasticceria / panetteria": "Bakery", "Negozio / e-commerce": "Store",
    "Immobiliare": "RealEstateAgent", "Commercialista": "AccountingService",
    "Commercialista / studio professionale": "ProfessionalService", "Studio legale": "LegalService",
}


# ── cosa mettere ─────────────────────────────────────────────────────────────

def schema(e: dict, kind: str | None) -> dict:
    ld = {"@context": "https://schema.org", "@type": kind or TYPES.get(e["vertical"], "LocalBusiness"),
          "name": e["name"]}
    for key, field in (("url", "website"), ("telephone", "phone"), ("address", "address"), ("hasMap", "maps_url")):
        if e.get(field):
            ld[key] = e[field]
    if e.get("rating") and e.get("review_count"):
        ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": e["rating"], "reviewCount": e["review_count"]}
    # Chi ha servizi si prenota; chi vende solo articoli (Negozio Kaio) si ordina.
    action, url = ("ReserveAction", e["booking_url"]) if e.get("booking_url") else ("OrderAction", e.get("shop_url"))
    if url:
        ld["potentialAction"] = {"@type": action, "target": {
            "@type": "EntryPoint", "urlTemplate": url,
            "actionPlatform": ["https://schema.org/DesktopWebPlatform", "https://schema.org/MobileWebPlatform"]}}
    return ld


def directory_entry(slug: str) -> dict | None:
    with urllib.request.urlopen(f"{API}/directory", timeout=30) as r:
        return next((e for e in json.load(r) if e["slug"] == slug), None)


# ── TanStack Start ───────────────────────────────────────────────────────────

def tsx_script(src: str, name: str, slug: str) -> str:
    """Aggiunge <CDN>/<name> accanto a k.js, nello stesso stile del sito (useEffect add() o <script> nel head)."""
    if name in src:
        return src
    url = f"{CDN}/{name}"
    # Stile useEffect: add("…/k.js", { kaio: X });
    m = re.search(r'\n(\s*)add\("' + re.escape(CDN) + r'/k\.js", \{ kaio: ([^}]+?) \}\);', src)
    if m:
        return src[:m.end()] + f'\n{m.group(1)}add("{url}", {{ kaio: {m.group(2)} }});' + src[m.end():]
    # Stile head: <script defer src="…/k.js" data-kaio=… />, anche su più righe
    m = re.search(r'\n(\s*)<script\b[^>]*?' + re.escape(CDN) + r'/k\.js[^>]*?/>', src, re.S)
    if m:
        kaio = re.search(r'data-kaio=(\{[^}]+\}|"[^"]+")', m.group(0)).group(1)
        return src[:m.end()] + f'\n{m.group(1)}<script defer src="{url}" data-kaio={kaio} />' + src[m.end():]
    # Niente k.js: va subito dopo <HeadContent /> (TanStack) o dentro <head> (Next)
    m = re.search(r'\n(\s*)<HeadContent />', src) or re.search(r'\n(\s*)<head>', src)
    if not m:
        return src  # chi chiama lo segnala come DA FARE
    return src[:m.end()] + f'\n{m.group(1)}<script defer src="{url}" data-kaio="{slug}" />' + src[m.end():]


def proxy_llms_vite(vite: Path, slug: str) -> str:
    src = vite.read_text()
    if "/llms.txt" in src:
        return "già presente"
    rule = f'nitro({{ routeRules: {{ "/llms.txt": {{ proxy: "{API}/geo/{slug}/llms.txt" }} }} }})'
    if "nitro()" not in src:
        return f"DA FARE: non trovo nitro() in vite.config, aggiungi a mano {rule}"
    vite.write_text(src.replace("nitro()", rule, 1))
    return "/llms.txt → Kaio"


def json_ld_tanstack(site: Path, root: Path, ld: dict) -> str:
    if any("ld+json" in p.read_text(errors="ignore") for p in (site / "src").rglob("*.tsx")):
        return "già presente, lasciato com'è"
    src = root.read_text()
    head = src.find("head: () =>")
    m = re.search(r"\n(\s+)links: \[", src[head:]) if head >= 0 else None
    if not m:
        return "DA FARE: non trovo links: [ dentro head, aggiungi a mano lo script ld+json"
    src = src.replace("export const Route", scheda_const(ld) + "export const Route", 1)
    at = src.index("head: () =>")
    at += re.search(r"\n\s+links: \[", src[at:]).start() + 1
    root.write_text(src[:at] + f'{m.group(1)}scripts: [{{ type: "application/ld+json", children: JSON.stringify(SCHEDA) }}],\n' + src[at:])
    return "aggiunto"


def scheda_const(ld: dict) -> str:
    return ("// Scheda per Google e per gli assistenti AI (GEO Kaio): chi siamo e dove si prenota.\n"
            f"const SCHEDA = {json.dumps(ld, ensure_ascii=False, indent=2)};\n\n")


# ── Next.js e HTML statico: /llms.txt lo serve Vercel ────────────────────────

def rewrite_vercel(site: Path, slug: str) -> str:
    """Su Vercel una rewrite basta per qualsiasi framework: /llms.txt → l'API di Kaio."""
    path = site / "vercel.json"
    conf = json.loads(path.read_text()) if path.exists() else {}
    rules = conf.setdefault("rewrites", [])
    if any(r.get("source") == "/llms.txt" for r in rules):
        return "già presente"
    rules.insert(0, {"source": "/llms.txt", "destination": f"{API}/geo/{slug}/llms.txt"})
    path.write_text(json.dumps(conf, indent=2, ensure_ascii=False) + "\n")
    return "/llms.txt → Kaio (vercel.json)"


def json_ld_next(layout: Path, ld: dict) -> str:
    src = layout.read_text()
    if "ld+json" in src:
        return "già presente, lasciato com'è"
    m = re.search(r"\n(\s*)<head>", src)
    if not m:
        return "DA FARE: non trovo <head> in layout, aggiungi a mano lo script ld+json"
    src = re.sub(r"^(export default )", scheda_const(ld) + r"\1", src, count=1, flags=re.M)
    tag = f'\n{m.group(1)}  <script type="application/ld+json" dangerouslySetInnerHTML={{{{ __html: JSON.stringify(SCHEDA) }}}} />'
    m = re.search(r"\n(\s*)<head>", src)
    layout.write_text(src[:m.end()] + tag + src[m.end():])
    return "aggiunto"


def ensure_head_next(src: str) -> str:
    """Next App Router non ha <head> nel layout di default: lo aggiungiamo dentro <html>."""
    if re.search(r"<head>", src):
        return src
    m = re.search(r"\n(\s*)<html\b[^>]*>", src)
    if not m:
        return src
    ind = m.group(1)
    return src[:m.end()] + f"\n{ind}  <head>\n{ind}  </head>" + src[m.end():]


def html_script(src: str, name: str, slug: str) -> str:
    if name in src:
        return src
    tag = f'    <script defer src="{CDN}/{name}" data-kaio="{slug}"></script>\n'
    return src.replace("</head>", tag + "</head>", 1) if "</head>" in src else src


def json_ld_html(page: Path, ld: dict) -> str:
    src = page.read_text()
    if "ld+json" in src:
        return "già presente, lasciato com'è"
    if "</head>" not in src:
        return "DA FARE: non trovo </head>"
    tag = f'    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    page.write_text(src.replace("</head>", tag + "</head>", 1))
    return "aggiunto"


# ── controlli finali ─────────────────────────────────────────────────────────

def site_kind(site: Path) -> tuple[str, Path]:
    for rel, kind in (("src/routes/__root.tsx", "tanstack"), ("app/layout.tsx", "next"), ("src/app/layout.tsx", "next"),
                      ("index.html", "html"), ("public/index.html", "html")):
        if (site / rel).exists():
            return kind, site / rel
    sys.exit(f"{site}: non trovo src/routes/__root.tsx, app/layout.tsx né index.html — che sito è?")


def leftovers(site: Path, text: str, chat: bool, main: Path) -> list[str]:
    todo = []
    lovable = [n for n in (".lovable", "bun.lock", "bunfig.toml", "src/lib/lovable-error-reporting.ts")
               if (site / n).exists()]
    agents = site / "AGENTS.md"  # il nostro si tiene, quello generato da Lovable no
    if agents.exists() and "lovable" in agents.read_text(errors="ignore").lower():
        lovable.append("AGENTS.md")
    pkg = site / "package.json"
    if pkg.exists() and "lovable" in pkg.read_text(errors="ignore"):
        lovable.append("@lovable.dev in package.json")
    if lovable:
        todo.append("via Lovable (passo 1 della ricetta sito-cliente): " + ", ".join(lovable))
    if not [p for p in site.rglob("privacy.*") if "node_modules" not in p.parts]:
        todo.append("/privacy: copia legal/privacy.tsx (o scrivi la pagina) e compila L con i dati veri del titolare (P.IVA da VIES)")
    if not re.search(r"P\.\s?IVA", text):
        todo.append("footer: © anno · ragione sociale · P.IVA · sede + link Privacy · Cookie")
    if "noindex" in text:
        todo.append("noindex attivo: va tolto solo con offerta firmata e P.IVA")
    if "k.js" not in main.read_text(errors="ignore"):
        todo.append(f"k.js non inserito: aggiungi a mano <script defer src=\"{CDN}/k.js\" data-kaio=\"<slug>\"> nel <head>")
    todo.append("chat e widget rispondono solo dal dominio vero: controlla allowed_origins (PATCH /admin/kaio/clients/{org}/business)")
    return todo


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", type=Path)
    ap.add_argument("slug")
    ap.add_argument("--no-chat", action="store_true", help="senza chat Kaio")
    ap.add_argument("--type", help="tipo schema.org, se quello dedotto dalla specialità non va")
    a = ap.parse_args()
    kind, main_file = site_kind(a.site)
    print(f"sito: {kind} ({main_file.relative_to(a.site)})")
    todo: list[str] = []

    src = main_file.read_text()
    if kind == "html":
        new = html_script(src, "k.js", a.slug)
        new = new if a.no_chat else html_script(new, "kchat.js", a.slug)
    else:
        new = ensure_head_next(src) if kind == "next" else src
        new = tsx_script(new, "k.js", a.slug)
        new = new if a.no_chat else tsx_script(new, "kchat.js", a.slug)
    main_file.write_text(new)
    print("k.js:", "già presente" if "k.js" in src else ("aggiunto" if "k.js" in new else "NON inserito"))
    if not a.no_chat:
        print("chat Kaio:", "già presente" if "kchat.js" in src else ("aggiunta" if "kchat.js" in new else "NON inserita"))

    entry = directory_entry(a.slug)
    if entry is None:
        todo.append(f"GEO: {a.slug} non è nella directory Kaio (pagina attiva, almeno un servizio o articolo attivo?), poi rilancia")
    else:
        ld = schema(entry, a.type)
        if kind == "tanstack":
            print("GEO llms.txt:", proxy_llms_vite(a.site / "vite.config.ts", a.slug))
            print("GEO JSON-LD:", json_ld_tanstack(a.site, main_file, ld))
        elif kind == "next":
            print("GEO llms.txt:", rewrite_vercel(a.site, a.slug))
            print("GEO JSON-LD:", json_ld_next(main_file, ld))
        else:
            print("GEO llms.txt:", rewrite_vercel(a.site, a.slug))
            print("GEO JSON-LD:", json_ld_html(main_file, ld))
        static = a.site / "public/llms.txt"
        if static.exists():
            static.unlink()
            print("public/llms.txt statico: tolto, copriva il proxy")
        if not entry.get("website"):
            todo.append("Kaio: «Presenza online» senza sito, metti l'URL (PUT /admin/kaio/clients/{org}/online)")

    print("font locali:", end=" ", flush=True)
    subprocess.run([sys.executable, str(HERE / "legal/fonts_local.py"), str(a.site)], check=True)
    print("ok")

    text = "".join(p.read_text(errors="ignore") for p in list(a.site.rglob("*.tsx")) + list(a.site.rglob("*.html"))
                   if "node_modules" not in p.parts and ".next" not in p.parts and "dist" not in p.parts)
    todo += leftovers(a.site, text, not a.no_chat, main_file)
    print("\nDA FARE:\n- " + "\n- ".join(todo))


if __name__ == "__main__":
    main()
