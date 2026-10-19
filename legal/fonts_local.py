"""Porta i Google Fonts di un sito in locale (public/fonts): niente IP dei visitatori a Google.
Uso: python3 fonts_local.py <cartella sito>
Cerca in src/routes/__root.tsx (TanStack Start), app/layout.tsx e src/app/layout.tsx (Next.js), index.html e public/index.html."""
import pathlib, re, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
site = pathlib.Path(sys.argv[1])
out = site / "public/fonts"
CANDIDATES = ("src/routes/__root.tsx", "app/layout.tsx", "src/app/layout.tsx", "index.html", "public/index.html")
files = [site / rel for rel in CANDIDATES if (site / rel).exists()]
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA)).read()

for f in files:
    src = f.read_text()
    urls = re.findall(r'https://fonts\.googleapis\.com/css2\?[^"\'\s]+', src)
    if not urls:
        continue
    css = []
    for u in urls:
        # tieni solo latin e latin-ext: gli altri alfabeti non servono
        for subset, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", get(u.replace("&amp;", "&")).decode(), re.S):
            if subset not in ("latin", "latin-ext"):
                continue
            def local(m):
                name = m.group(1).rsplit("/", 1)[1]
                out.mkdir(parents=True, exist_ok=True)
                (out / name).write_bytes(get(m.group(1)))
                return f"url(/fonts/{name})"
            css.append(re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", local, block))
    (out / "fonts.css").write_text("\n".join(css) + "\n")
    for u in urls:
        src = src.replace(u, "/fonts/fonts.css")
    src = re.sub(r'\{[^{}]*fonts\.(?:googleapis|gstatic)\.com"[^{}]*\},?\s*', "", src)
    src = re.sub(r'<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*', "", src)
    f.write_text(src)
    print(f"{f}: {len(urls)} css → {len(list(out.glob('*.woff2')))} woff2 in public/fonts")
