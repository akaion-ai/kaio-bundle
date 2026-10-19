# Glossario, per chi non fa questo di mestiere

**Agente** — un assistente IA che non si limita a rispondere: legge file, lancia comandi, modifica cose. Claude Code, Codex e Cursor sono agenti.

**allowed_origins** — l'elenco dei siti da cui Kaio accetta di mostrare il widget e la chat. Se il dominio del cliente non c'è, compare «embed non autorizzato».

**Bundle** — il pacchetto di cose che il sito del cliente deve avere per lavorare con Kaio: visite, chat, prenotazioni, GEO, font locali, privacy.

**Commit / push** — in git, «salva questa versione» (commit) e «mandala su GitHub» (push). Dopo il push, Vercel pubblica il sito da solo.

**Deploy** — pubblicare il sito online. Con Vercel succede da solo a ogni push sul ramo `main`.

**Dominio** — l'indirizzo del sito, es. `www.cinziaestetica.it`. Finché il cliente non ne compra uno, il sito vive su `nome.vercel.app`.

**GEO** — *Generative Engine Optimization*: farsi trovare dagli assistenti IA come ci si fa trovare da Google. Per Kaio sono due cose: il file `/llms.txt` (listino e orari in testo semplice, letti da ChatGPT/Claude) e la scheda `schema.org` nascosta nella pagina.

**git / GitHub** — git è il sistema che tiene la storia dei file di un sito; GitHub è il sito dove quella storia sta online. I siti dei clienti sono in `github.com/akaion-ai`.

**JSON-LD / schema.org** — un blocco invisibile nella pagina che dice a Google e alle IA «questa è un'estetista, si chiama così, telefono, indirizzo, si prenota qui».

**k.js / kchat.js** — i due piccoli programmi di Kaio che il sito carica: il primo conta le visite senza cookie, il secondo è la chat.

**llms.txt** — vedi GEO.

**MCP** — *Model Context Protocol*. La «presa» standard con cui un assistente IA si collega a un servizio. Akaion ne ha due: uno per chi lavora con Kaio (con login) e uno pubblico per cercare e prenotare.

**noindex** — un'istruzione nella pagina che dice a Google «non mostrarmi nei risultati». Si tiene finché il sito non è a norma e l'offerta non è firmata.

**OAuth** — il tipo di login «entra con il tuo account» che si apre nel browser quando colleghi un MCP. Non dai mai la password all'assistente.

**P.IVA / VIES** — la partita IVA del titolare, obbligatoria nel footer del sito. VIES è il sito europeo dove si verifica che esista.

**Repo** — una cartella di progetto seguita da git. Un sito = un repo.

**Slug** — il nome corto dell'attività nei link di Kaio: in `smallbusiness.akaion.com/cinzia-estetica` lo slug è `cinzia-estetica`.

**Terminale** — la finestra nera dove si scrivono comandi. Su Mac si chiama Terminale, su Windows PowerShell.

**Vercel** — il servizio che tiene online i siti dei clienti. Il team Akaion si chiama `akaion-projects`.

**Widget** — il calendario di prenotazione Kaio incorporato nel sito.
