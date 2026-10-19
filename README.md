# Bundle Kaio

Tutto quello che serve per collegare il sito di una piccola attività a **Kaio by Akaion**, in un comando, fatto da una persona o da un agente (Claude Code, Codex, Cursor o un assistente con MCP).

Il bundle mette sul sito:

- **k.js** — conteggio visite senza cookie, che il titolare vede nella «Presenza online» dell'app Kaio;
- **kchat.js** — la chat Kaio: risponde su servizi, prezzi, orari e posti liberi di quell'attività e porta a prenotare;
- **GEO** — `/llms.txt` con listino e orari sempre aggiornati da Kaio e la scheda `schema.org` nel `<head>`: così ChatGPT, Claude e Perplexity trovano l'attività e sanno dove prenotare;
- **font locali** — niente Google Fonts dal browser, zero cookie e zero terze parti: il banner cookie non serve;
- **kit legale** — pagina `/privacy` (privacy, cookie, uso dell'IA, condizioni di vendita) e il footer con i dati del titolare.

Funziona su siti **TanStack Start** (quelli usciti da Lovable), **Next.js** (App Router) e **HTML statico**. Solo Python standard, nessuna dipendenza.

## Se non sei una persona tecnica

Non devi scrivere codice. Ti serve un assistente che sappia usare questo repo. Scegli la tua strada in `docs/`:

| Vuoi… | Leggi |
|---|---|
| far fare tutto a Claude Code sul tuo computer (consigliato) | [docs/setup-claude-code.md](docs/setup-claude-code.md) |
| gestire l'attività su Kaio parlando con Claude (app desktop o web) | [docs/setup-claude-desktop.md](docs/setup-claude-desktop.md) |
| lo stesso, ma con ChatGPT | [docs/setup-chatgpt.md](docs/setup-chatgpt.md) |
| usare Cursor o un altro agente | [docs/setup-altri-agenti.md](docs/setup-altri-agenti.md) |
| capire le parole (MCP, slug, deploy, noindex…) | [docs/glossario.md](docs/glossario.md) |

## Se sei tecnico: in tre righe

```sh
git clone https://github.com/akaion-ai/kaio-bundle.git
python3 kaio-bundle/bundle_install.py <cartella del sito> <slug Kaio> [--no-chat] [--type BeautySalon]
# poi: build, commit, push. L'installer stampa i «DA FARE» che non può chiudere da solo.
```

Lo `slug` è la fine del link di prenotazione dell'attività: `https://smallbusiness.akaion.com/<slug>`. L'attività deve essere attiva su Kaio con almeno un servizio o un articolo, altrimenti il GEO viene saltato (l'installer lo dice, lo rilanci dopo).

## Come skill o plugin di Claude Code

```sh
# plugin (consigliato): porta la skill e il server MCP di Akaion
claude plugin marketplace add akaion-ai/kaio-bundle
claude plugin install kaio@akaion-kaio

# oppure solo la skill, copiata a mano
curl -fsSL https://raw.githubusercontent.com/akaion-ai/kaio-bundle/main/install.sh | sh
```

Poi in Claude Code: `/kaio:kaio-bundle` (plugin) o `/kaio-bundle` (skill copiata), e dici su quale sito e con quale slug. La procedura completa che l'agente segue è in [skills/kaio-bundle/SKILL.md](skills/kaio-bundle/SKILL.md): vale anche come checklist per una persona.

## Cosa c'è dentro

```
bundle_install.py        l'installer (riconosce il tipo di sito da solo)
legal/privacy.tsx        pagina /privacy per TanStack Start: compila l'oggetto L in cima
legal/fonts_local.py     porta i Google Fonts in public/fonts
skills/kaio-bundle/      la skill per Claude Code (procedura completa, MCP compresi)
.claude-plugin/          manifest plugin + marketplace
.mcp.json                il server MCP di Akaion (si collega con /mcp in Claude Code)
docs/                    guide passo passo per chi non è tecnico
tests/                   un controllo senza rete sui tre tipi di sito: python3 -m pytest tests
AGENTS.md                le stesse istruzioni, corte, per Codex/Cursor/altri agenti
```

## Gli MCP di Akaion

| Server | Chi lo usa | URL |
|---|---|---|
| **Akaion** (staff e titolari Kaio, login OAuth) | configurare attività, listini, orari; il titolare legge la propria attività | `https://api.website.prod.akaion.com/mcp` |
| **Kaio** (pubblico, senza login) | chiunque, in ChatGPT o Claude: cerca attività, vede posti liberi, prenota | `https://api.website.prod.akaion.com/mcp/kaio` |

Dettagli e strumenti: [smallbusiness.akaion.com/app-ai](https://smallbusiness.akaion.com/app-ai).

## Regole che non si saltano

- Niente scritture su Kaio in produzione senza il sì di chi segue il cliente.
- Mai inventare una P.IVA o una ragione sociale: senza i dati veri il sito resta `noindex`.
- Niente recensioni, numeri o prezzi d'esempio online. Niente foto o nomi di clienti veri negli esempi.
- Dopo il bundle non si aggiungono Google Fonts, iframe o pixel: la pagina Cookie smette di essere vera.

Supporto: akaion@akaion.com · © Akaion SRL. Uso libero per i clienti e i partner Kaio.
