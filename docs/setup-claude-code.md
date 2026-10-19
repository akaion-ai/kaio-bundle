# Claude Code: far fare tutto all'assistente, sul tuo computer

Claude Code è un programma che gira nel «Terminale» del computer e lavora sui file al posto tuo: scarica il sito, ci mette il bundle, lo pubblica. Tu gli parli in italiano. Questa guida parte da zero.

Tempo: 20 minuti la prima volta, 5 le successive.

## 1. Cosa devi avere

- Un Mac o un PC Windows con connessione a internet.
- Un account Claude (claude.ai) con piano Pro, Max o Team. Lo paga Akaion per gli specialist: chiedi a chi ti segue.
- L'account GitHub di Akaion per scaricare il sito del cliente: te lo abilita Akaion (invito su github.com, accetti dalla mail).
- Un account Akaion/Kaio con poteri da staff, per configurare le attività dei clienti via MCP. Te lo crea Akaion.

## 2. Installare Claude Code

Apri il **Terminale**:

- Mac: `cmd + spazio`, scrivi `Terminale`, invio.
- Windows: tasto Windows, scrivi `PowerShell`, invio.

Incolla questa riga e premi invio (Mac):

```sh
curl -fsSL https://claude.ai/install.sh | sh
```

Su Windows (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

Chiudi e riapri il Terminale. Scrivi `claude` e premi invio: la prima volta ti apre il browser per entrare con il tuo account Claude. Fatto. Per uscire da Claude Code si scrive `/exit`.

Se `claude` dice «comando non trovato», chiudi e riapri il Terminale ancora una volta. Se persiste, scrivi a chi ti segue con la foto dello schermo.

## 3. Installare il Bundle Kaio dentro Claude Code

Dentro Claude Code (dopo aver scritto `claude`), incolla una riga alla volta:

```
/plugin marketplace add akaion-ai/kaio-bundle
/plugin install kaio@akaion-kaio
```

Ora Claude Code conosce la procedura del bundle (`/kaio:kaio-bundle`) e ha il server MCP di Akaion.

## 4. Collegare il tuo account Akaion (MCP)

Un **MCP** è una presa: dà all'assistente il permesso di parlare con un servizio, qui Kaio. Senza, Claude può modificare il sito ma non può creare l'attività su Kaio.

Dentro Claude Code scrivi:

```
/mcp
```

Scegli `akaion` dalla lista e premi invio su **Authenticate**. Si apre il browser: entri con l'account Akaion/Kaio (quello da staff). Torna al Terminale: deve dire `connected`.

Prova: scrivi «chi sono per Akaion?». Claude usa `whoami` e ti risponde con il tuo account e se hai poteri da staff.

## 5. Scaricare il sito del cliente

I siti dei clienti stanno su GitHub, nell'organizzazione `akaion-ai`. Ogni sito è un «repo» con un nome tipo `cinzia_estetica`. Ti serve il nome: te lo dice chi ha fatto il sito, oppure lo vedi su github.com/akaion-ai.

Nel Terminale (fuori da Claude Code, o chiedendo a Claude di farlo):

```sh
mkdir -p ~/Desktop/clienti && cd ~/Desktop/clienti
git clone https://github.com/akaion-ai/<nome-del-repo>.git
cd <nome-del-repo>
claude
```

La prima volta `git` ti chiede di entrare in GitHub: segui le istruzioni a schermo (apre il browser).

## 6. Dire a Claude cosa fare

Ora sei dentro la cartella del sito, dentro Claude Code. Scrivi, con parole tue:

> Installa il bundle Kaio su questo sito. L'attività è «Cinzia Estetica», slug Kaio `cinzia-estetica`. Dominio vero: https://www.cinziaestetica.it

Se l'attività non è ancora su Kaio:

> L'attività non è ancora su Kaio: creala. Si chiama «Bar Pasticceria Rossi», pasticceria a Cassago Brianza, titolare Mario Rossi, mail mario@esempio.it, orari lun-sab 7-19. Poi metti il bundle sul sito.

Claude segue la procedura della skill: ti chiede conferma **prima di ogni scrittura su Kaio** (è giusto così: rispondi sì solo se è quello che vuoi), mette gli script, il GEO e i font locali, prepara il commit e il push. Alla fine ti elenca i «DA FARE»: tipicamente i dati legali del titolare (P.IVA, sede), che solo il cliente può darti.

## 7. Controllare che funzioni

Apri il sito dal dominio vero nel browser:

- in basso a destra c'è la bolla della chat Kaio; prova «quanto costa …?»;
- il bottone «Prenota» apre il calendario con i posti liberi veri;
- `https://<dominio>/llms.txt` mostra listino e orari (è quello che leggono ChatGPT e Claude).

Se la chat dice «embed non autorizzato», il dominio non è tra quelli autorizzati su Kaio: chiedi a Claude «aggiungi https://www.dominio.it agli allowed_origins dell'attività».

## Domande frequenti

**Devo capire il codice che Claude scrive?** No. Devi capire i DA FARE e procurarti i dati veri del cliente.

**Posso rompere qualcosa?** Sul sito no: ogni modifica passa da git e si può tornare indietro (`git revert`). Su Kaio sì se dici sì a una scrittura sbagliata: per questo Claude chiede conferma, e per questo si lavora sempre con il nome esatto dell'attività.

**Quanto costa?** Il piano Claude. Il bundle e gli MCP di Akaion sono gratuiti per clienti e partner.

**E se il cliente ha un sito WordPress o Wix?** Il bundle non lo installa da solo. Si passa da un sito nuovo (ricetta «sito-cliente» di Akaion) oppure si incollano a mano i due `<script>` nel tema: chiedi a chi ti segue.
