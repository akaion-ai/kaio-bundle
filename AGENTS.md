# Bundle Kaio — istruzioni per agenti

Scopo: collegare il sito di una piccola attività a Kaio by Akaion. Procedura completa in `skills/kaio-bundle/SKILL.md`; questa è la versione corta.

1. **Prerequisiti**: cartella del sito con git; slug Kaio (`https://smallbusiness.akaion.com/<slug>`); Python 3.9+. Se il sito ha `.lovable/` o `@lovable.dev` in package.json, prima va tolto da Lovable.
2. **Kaio** (solo se l'attività non esiste o va configurata, via MCP `https://api.website.prod.akaion.com/mcp`, strumenti `smallbusiness_admin_endpoints` + `smallbusiness_admin`): `POST /api/v1/admin/kaio/clients`, poi `PUT …/hours`, `PUT …/services/import` (o `PUT …/shop` + `…/shop/items/import`), `PATCH …/business {contact_phone, allowed_origins}`, `PUT …/online {place_id, website, instagram}`, `PUT …/reminders`. **Chiedi conferma prima di ogni scrittura.**
3. **Sito**: `python3 bundle_install.py <sito> <slug> [--no-chat] [--type <schema.org>]`. Riconosce TanStack Start / Next.js / HTML statico; mette k.js, kchat.js, `/llms.txt` → Kaio, JSON-LD, font locali. Rilanciabile. Leggi i **DA FARE** che stampa.
4. **Legale**: footer con `© anno · ragione sociale · P.IVA · sede` + link Privacy/Cookie; pagina `/privacy` da `legal/privacy.tsx` (compila `L`). Dati veri dal cliente, P.IVA verificata su VIES. Mai inventarli: senza, il sito resta `noindex`. Niente Google Fonts, iframe, pixel, recensioni o prezzi d'esempio.
5. **Verifica**: build; `curl https://<dominio>/llms.txt`; `grep ld+json`; dal dominio vero la chat compare (altrimenti aggiungi il dominio ad `allowed_origins`). Commit + push non forzato su `main`.
6. **Chiudi**: `PUT …/online {website}` con l'URL definitivo; riporta URL live, cosa è vero, cosa manca.
