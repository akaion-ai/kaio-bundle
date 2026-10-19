---
name: kaio-bundle
description: Installa il Bundle Kaio su un sito cliente (visite senza cookie, chat Kaio, prenotazioni, GEO per ChatGPT/Claude, font locali, note legali) e configura l'attività su Kaio via MCP. Usala quando qualcuno dice "metti Kaio sul sito", "bundle Kaio", "collega il sito a Kaio", "GEO", "fai trovare l'attività da ChatGPT", o porta un nuovo sito cliente.
when_to_use: Siti di piccole attività (estetiste, artigiani, negozi, studi) che prenotano o vendono con Kaio by Akaion. Funziona su TanStack Start, Next.js e HTML statico; il sito deve stare in una cartella locale con git.
---

# Bundle Kaio — procedura per l'agente

Fai le cose in questo ordine. Ogni passo si verifica prima del successivo.
Niente scritture su Kaio in produzione senza che la persona abbia detto sì a quel passo preciso.

## 0. Cosa ti serve prima di partire

| Cosa | Come lo ottieni |
|---|---|
| Cartella del sito | `git clone` del repo del cliente, in locale |
| Slug Kaio dell'attività | è la fine del link di prenotazione `https://smallbusiness.akaion.com/<slug>`; se l'attività non è ancora su Kaio, la crei al passo 1 |
| MCP Akaion collegato (solo per il passo 1 e il passo 5) | server `https://api.website.prod.akaion.com/mcp`, login con l'account Akaion/Kaio di chi lavora. Setup in `docs/setup-claude-code.md` |
| Python 3.9+ | `python3 --version` |

Se il sito è ancora su Lovable (`.lovable/`, `@lovable.dev` in package.json) prima si fa la ricetta "sito-cliente" passo 1 (de-Lovable). L'installer te lo segnala tra i DA FARE.

## 1. L'attività su Kaio (via MCP Akaion, serve essere staff Akaion)

Prima `smallbusiness_admin_endpoints` per avere la lista aggiornata, poi `smallbusiness_admin` con questi, nell'ordine. Base: `/api/v1/admin/kaio`.

1. **Esiste già?** `GET /orgs` e cerca il nome. Se c'è, prendi `org_id` e `slug` e salta alla 3.
2. **Crea il cliente** `POST /clients` con `{business_name, vertical, timezone:"Europe/Rome", owner:{name, email, password}}`. Il `vertical` è una delle specialità di Kaio (Estetista, Fisioterapista, Edilizia, Negozio / e-commerce, Pasticceria / panetteria, …). La password è quella provvisoria del titolare: gliela mandi a voce o su WhatsApp, mai in chiaro in una mail. La risposta dà `org.id` e `booking_page.slug`.
3. **Orari** `PUT /clients/{org_id}/hours` `{hours:[{day_of_week:0..6, start:"09:00", end:"19:00"}, …]}` (0 = lunedì; due fasce nello stesso giorno = due righe).
4. **Listino** `PUT /clients/{org_id}/services/import` `{services:[{name, duration_minutes, price_cents}]}` per chi lavora su appuntamento. Chi vende articoli (bottega, pizzeria d'asporto, negozio): `PUT /clients/{org_id}/shop` `{offering:"products", payment:"none"|"optional"|"required", intro, pickup_slots}` e `PUT /clients/{org_id}/shop/items/import`. `POST …/shop/items/autofill` propone gli articoli leggendo il sito, da rivedere prima di importare.
5. **Dati di contatto e dominio** `PATCH /clients/{org_id}/business` `{contact_phone, allowed_origins:["https://www.dominio.it","https://dominio.it"]}`. Senza il dominio in `allowed_origins` widget e chat sul sito dicono "embed non autorizzato". Aggiungi anche l'URL `*.vercel.app` finché il dominio vero non c'è.
6. **Presenza online** `GET /places/search?q=<nome città>` per trovare la scheda Google, poi `PUT /clients/{org_id}/online` `{place_id, website, instagram}`.
7. **Promemoria** `PUT /clients/{org_id}/reminders` `{rules:[{id:"m1440", minutes:1440, channels:["whatsapp","email"], enabled:true}]}`.
8. **Aspetto** `PUT /clients/{org_id}/appearance` `{accent:"#b0237c", mode:"light", radius:"soft", show_prices:true}` con il colore del sito.
9. **Agenti** (se venduti) `PUT /clients/{org_id}/agents` con la lista degli id attivi.

Verifica: `GET /clients/{org_id}` ha una sezione `readiness` con i punti aperti. L'attività compare in `https://api.prod.akaion.com/api/service1/api/v1/kaio/directory` solo se la pagina è attiva e ha almeno un servizio o articolo attivo: senza, il GEO del passo 2 salta.

## 2. Il bundle sul sito (un comando, nessuna rete di Kaio toccata)

```sh
python3 <radice di questo repo>/bundle_install.py <cartella sito> <slug> [--no-chat] [--type BeautySalon]
```

Dove sta lo script: installato come plugin → `${CLAUDE_PLUGIN_ROOT}/bundle_install.py`; skill copiata con `install.sh` → nella stessa cartella di questo SKILL.md; repo clonato → nella radice. Cercalo con `ls` prima di lanciarlo.

Cosa fa, e dove:

| Pezzo | TanStack Start | Next.js (App Router) | HTML statico |
|---|---|---|---|
| `k.js` visite senza cookie | `src/routes/__root.tsx` accanto a `<HeadContent />` o nel `useEffect` esistente | `app/layout.tsx` dentro `<head>` (lo crea se manca) | `index.html` prima di `</head>` |
| `kchat.js` chat Kaio | idem | idem | idem |
| `/llms.txt` vivo da Kaio | `vite.config.ts`: `nitro({ routeRules })` proxy | `vercel.json` rewrite | `vercel.json` rewrite |
| JSON-LD schema.org | `head.scripts` in `__root.tsx` | `<script type="application/ld+json">` nel layout | nel `<head>` |
| Font locali | `legal/fonts_local.py` scarica i Google Fonts in `public/fonts` e riscrive i link | idem | idem |

Si può rilanciare: quello che c'è già resta com'è. `--type` forza il tipo schema.org se quello dedotto dalla specialità non va (`Bakery`, `Store`, `Physiotherapy`, `GeneralContractor`, …).

Alla fine stampa i **DA FARE**: sono i punti che un programma non può chiudere da solo. Falli tutti o riportali alla persona, uno per uno.

## 3. A norma di legge (prima di mandare il link al cliente)

Il kit è in `legal/`. Finché un punto resta aperto il sito resta `noindex`.

- **Dati veri del titolare**: ragione sociale esatta, P.IVA verificata su VIES (https://ec.europa.eu/taxation_customs/vies/), sede legale; REA e capitale per le società; albo per le professioni regolamentate. Prima fonte: il cliente. **Mai inventare una P.IVA**: senza, il sito non va online col nome del cliente.
- **Footer di ogni pagina**: `© anno · Ragione sociale · P.IVA … · sede` + link `Privacy · Cookie` a `/privacy` e `/privacy#cookie`.
- **`/privacy`**: copia `legal/privacy.tsx` in `src/routes/` (TanStack) e compila l'oggetto `L` in cima (`kaio`, `vendita` ritiro/spedizione, `ia`, `sanitario`, `albo`, `whatsapp`). Su Next o HTML riscrivi la stessa struttura: titolare, privacy art. 13 GDPR, cookie, IA (art. 50 AI Act), condizioni di vendita se vende. Contatto privacy di default `privacy@akaion.com`.
- **Zero cookie, zero terze parti**: niente iframe Google Maps/YouTube/Instagram (link al posto dell'iframe), niente Analytics/pixel, immagini servite dal sito. Così il banner cookie non serve. Kaio stesso è senza cookie.
- **Contenuti veri**: niente recensioni, numeri («20 anni», «500 clienti»), premi senza fonte. Niente prezzi d'esempio: o il listino vero o nessun prezzo. Cibo: allergeni per ogni articolo (campo allergeni di Kaio). Sanità: solo informazioni, nessuna promessa di risultato.
- **Prospect** (offerta non firmata): `noindex` + Vercel Deployment Protection, mai il nome del cliente online senza il suo OK.

## 4. Build, verifica, deploy

```sh
npm install && npm run build            # TanStack / Next
git add -A && git commit -m "Bundle Kaio: k.js, chat, GEO, font locali" && git push
```

Dopo il deploy (Vercel deploya da `main`):

```sh
curl -s https://<dominio>/llms.txt | head -20      # listino e orari vivi da Kaio
curl -s https://<dominio>/ | grep -o 'ld+json'        # scheda JSON-LD presente
curl -s https://<dominio>/ | grep -o 'k.js\|kchat.js' # script presenti
```

Poi apri il sito **dal dominio vero**, con la scheda in primo piano: deve comparire la bolla della chat in basso a destra e il widget di prenotazione deve rispondere. In locale «embed non autorizzato» è normale.

## 5. Chiusura su Kaio

- `PUT /clients/{org_id}/online` con il `website` definitivo, così la «Presenza online» del titolare conta le visite giuste.
- Dì al titolare come entrare: app Kaio (App Store / Google Play) o `https://smallbusiness.akaion.com`, con la mail e la password provvisoria; al primo accesso la cambia.
- Riporta alla persona: URL live, cosa è vero e cosa è da confermare col cliente, DA FARE rimasti.

## Cosa NON fare

- Non scrivere su Kaio in produzione senza un sì esplicito a quel passo.
- Non usare `--force` su git: Lovable può essere ancora collegato al repo.
- Non pubblicare foto o nomi di clienti veri negli esempi o negli screenshot.
- Non mettere un Google Font, un iframe o un pixel dopo l'installazione: la pagina Cookie smette di essere vera.
