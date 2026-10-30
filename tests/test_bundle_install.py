"""Un controllo solo, senza rete: l'installer tocca i tre tipi di sito nel punto giusto e non duplica se rilanciato."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bundle_install as b  # noqa: E402

ENTRY = {"name": "Prova Estetica", "slug": "prova", "vertical": "Estetista", "website": "https://prova.it", "phone": "+39 02 1",
         "address": None, "maps_url": None, "rating": 4.9, "review_count": 12, "booking_url": "https://smallbusiness.akaion.com/prova"}


def test_schema_reserve():
    ld = b.schema(ENTRY, None)
    assert ld["@type"] == "BeautySalon"
    assert ld["potentialAction"]["@type"] == "ReserveAction"
    assert ld["aggregateRating"]["reviewCount"] == 12


def test_html(tmp_path):
    page = tmp_path / "index.html"
    page.write_text("<html><head><title>x</title></head><body></body></html>")
    src = b.html_script(page.read_text(), "k.js", "prova")
    src = b.html_script(src, "kchat.js", "prova")
    assert src.count("k.js") == 1 and src.count("kchat.js") == 1
    assert b.html_script(src, "k.js", "prova") == src  # idempotente
    page.write_text(src)
    assert b.json_ld_html(page, b.schema(ENTRY, None)) == "aggiunto"
    assert b.json_ld_html(page, b.schema(ENTRY, None)).startswith("già")
    assert b.rewrite_vercel(tmp_path, "prova").endswith("(vercel.json)")
    assert json.loads((tmp_path / "vercel.json").read_text())["rewrites"][0]["source"] == "/llms.txt"
    assert b.rewrite_vercel(tmp_path, "prova") == "già presente"


def test_next(tmp_path):
    layout = tmp_path / "app/layout.tsx"
    layout.parent.mkdir(parents=True)
    layout.write_text('export default function RootLayout({ children }) {\n  return (\n    <html lang="it">\n      <body>{children}</body>\n    </html>\n  );\n}\n')
    src = b.ensure_head_next(layout.read_text())
    src = b.tsx_script(src, "k.js", "prova")
    src = b.tsx_script(src, "kchat.js", "prova")
    assert "<head>" in src and src.count("k.js") == 1 and "kchat.js" in src
    layout.write_text(src)
    assert b.json_ld_next(layout, b.schema(ENTRY, None)) == "aggiunto"
    assert "const SCHEDA" in layout.read_text() and layout.read_text().index("const SCHEDA") < layout.read_text().index("export default")


def test_tanstack(tmp_path):
    root = tmp_path / "src/routes/__root.tsx"
    root.parent.mkdir(parents=True)
    root.write_text('export const Route = createRootRoute({\n  head: () => ({\n    meta: [],\n    links: [],\n  }),\n});\nfunction R() {\n  return (\n    <html>\n      <head>\n        <HeadContent />\n      </head>\n    </html>\n  );\n}\n')
    (tmp_path / "vite.config.ts").write_text("export default defineConfig({ plugins: [nitro()] });\n")
    src = b.tsx_script(root.read_text(), "k.js", "prova")
    assert '<HeadContent />\n        <script defer src="https://smallbusiness.akaion.com/k.js" data-kaio="prova" />' in src
    root.write_text(src)
    assert b.proxy_llms_vite(tmp_path / "vite.config.ts", "prova") == "/llms.txt → Kaio"
    assert "routeRules" in (tmp_path / "vite.config.ts").read_text()
    assert b.json_ld_tanstack(tmp_path, root, b.schema(ENTRY, None)) == "aggiunto"
    assert "scripts: [{ type: \"application/ld+json\"" in root.read_text()


def test_style_immersive(tmp_path):
    css = tmp_path / "src/styles.css"
    css.parent.mkdir(parents=True)
    css.write_text('@import "tailwindcss";\n@import "tw-animate-css";\n\nbody { color: red; }\n')
    b.style_immersive(tmp_path, "tanstack", tmp_path / "src/routes/__root.tsx")
    b.style_immersive(tmp_path, "tanstack", tmp_path / "src/routes/__root.tsx")  # idempotente
    lines = css.read_text().splitlines()
    assert lines[2] == '@import "./kaio-immersive.css";' and css.read_text().count("kaio-immersive") == 1
    assert ".im-hero" in (tmp_path / "src/kaio-immersive.css").read_text()
