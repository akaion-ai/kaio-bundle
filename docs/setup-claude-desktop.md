# Claude (app o web): gestire Kaio parlando

Qui non si tocca il sito. Si usa Claude come se fosse un collega che ha accesso al pannello di Kaio: «crea l'attività», «aggiorna il listino», «quali clienti non hanno ancora il sito collegato?». Serve l'account Claude (Pro, Max o Team) e l'account Akaion/Kaio.

## 1. Aggiungere il connettore Akaion

Un **connettore** è lo stesso concetto dell'MCP: una presa che dà a Claude il permesso di parlare con Kaio a nome tuo.

1. Apri claude.ai (o l'app Claude per Mac/Windows/iPhone).
2. In basso a sinistra, il tuo nome → **Impostazioni** → **Connettori**.
3. **Aggiungi connettore personalizzato**.
4. Nome: `Akaion`. URL: `https://api.website.prod.akaion.com/mcp`. Salva.
5. Premi **Connetti**: si apre la pagina di accesso di Akaion. Entra con il tuo account Akaion/Kaio.

Torna in chat. Nella barra degli allegati (icona +) ora c'è «Akaion» con i suoi strumenti. Lasciali tutti accesi.

## 2. Il connettore Kaio pubblico (facoltativo)

Serve per fare quello che fa un cliente finale: cercare un'estetista in zona, vedere i posti liberi, prenotare. Non ha login.

Stesso percorso: **Aggiungi connettore personalizzato**, nome `Kaio`, URL `https://api.website.prod.akaion.com/mcp/kaio`. Utile per far vedere al titolare come la sua attività compare in Claude.

## 3. Cosa puoi chiedere

Con il connettore Akaion collegato come **staff**:

- «Elenca le attività Kaio e dimmi quali non hanno il sito in Presenza online.»
- «Crea l'attività "Fisio Besana" di Simone Casati, fisioterapista, orari lun-ven 8-20, titolare simone@esempio.it.» (Claude ti chiede conferma prima di creare.)
- «Importa questo listino su Fisio Besana: Valutazione 60 min 70 €, Seduta 45 min 55 €.»
- «Collega la scheda Google di Fisio Besana a Besana in Brianza e il sito https://fisiobesana.vercel.app.»
- «Aggiungi https://www.fisiobesana.it ai domini autorizzati di Fisio Besana.»
- «Attiva i promemoria 24 ore prima via WhatsApp ed email.»

Come **titolare Kaio** (senza poteri staff): «Che servizi ho a listino?», «Quali posti liberi ho domani?», «Com'è la mia presenza online?», «Carica questo listino» (ti chiede conferma).

## 4. Regole

- Claude chiede conferma prima di scrivere su Kaio. Leggi cosa sta per fare e di' sì solo se è esatto: nome dell'attività, prezzi, orari.
- Niente dati di clienti finali in chat: Claude non li vede e non servono.
- Il bundle sul sito (script, GEO, privacy) non si fa da qui: serve Claude Code, vedi `setup-claude-code.md`.

## Se qualcosa non va

- «Connettore non raggiungibile»: riprova tra un minuto; se persiste scrivi a akaion@akaion.com.
- Claude dice che non hai poteri da staff: il tuo account Akaion non è nell'organizzazione Akaion su Kaio. Chiedi a chi ti segue di aggiungerti.
- Il login si apre ma torna indietro con un errore: controlla di usare la mail con cui sei stato aggiunto, non una personale.
