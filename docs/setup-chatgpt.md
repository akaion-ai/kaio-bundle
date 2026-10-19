# ChatGPT: Kaio come app

ChatGPT può usare gli stessi server MCP di Akaion. È la via più semplice per far vedere a un titolare come la sua attività appare «dentro l'IA»: cerchi, vedi i posti liberi veri, prenoti.

## 1. Kaio pubblico (per tutti, senza login)

1. Cerca «Kaio» tra le app di ChatGPT e aggiungila. Se non la trovi:
2. Impostazioni → **App e connettori** → **Impostazioni avanzate** → attiva **Modalità sviluppatore**.
3. Torna in **App e connettori** → **Crea**. Nome `Kaio`, URL `https://api.website.prod.akaion.com/mcp/kaio`, autenticazione **Nessuna**. Crea.

Prova in una chat nuova: «cerca un'estetista in Brianza e dimmi i posti liberi sabato per una manicure». Prima di prenotare ChatGPT riepiloga tutto e aspetta il tuo sì.

## 2. Akaion (staff e titolari, con login)

Stesso percorso, **Crea** con URL `https://api.website.prod.akaion.com/mcp` e autenticazione **OAuth**. Al primo uso ChatGPT ti manda alla pagina di accesso di Akaion: entra con l'account Akaion/Kaio.

Cosa chiedere: le stesse cose di `setup-claude-desktop.md`, sezione 3.

## 3. Cosa non si fa da ChatGPT

Il bundle sul sito del cliente (script, GEO, pagina privacy) richiede di modificare file e pubblicarli: lo fa Claude Code (vedi `setup-claude-code.md`) o un altro agente con accesso al repo (`setup-altri-agenti.md`).

## Note

- Una sola prenotazione di prova si fa sempre sull'attività demo «Akaion», mai su un cliente vero.
- Se l'app chiede «dati per il pagamento», non è la nostra: Kaio non chiede mai pagamenti dentro la chat, al massimo dà un link alla pagina Stripe dell'attività su smallbusiness.akaion.com.
