import { createFileRoute, Link } from "@tanstack/react-router";
import type { ReactNode } from "react";

// Note legali del sito: privacy (art. 13 GDPR), cookie, uso dell'IA (art. 50
// Reg. UE 2024/1689) e, se il sito vende, condizioni di vendita.
// Copiato dal kit .claude/skills/sito-cliente/legal: compila solo L.
// Il sito non deve avere cookie né script di terzi (font in locale, niente
// iframe Google Maps/YouTube/Instagram): se ne aggiungi uno, la sezione Cookie
// non è più vera e serve il banner di consenso.
const L = {
  sito: "__SITO__", // es. cinziaestetica.it
  titolare: "__TITOLARE__", // ragione sociale esatta, es. "Cinzia Estetica di Lofaro Cinzia"
  piva: "__PIVA__",
  sede: "__SEDE__", // sede legale completa
  rea: "" as string, // solo società, es. "LC-123456"
  capitale: "" as string, // solo srl/spa, es. "10.000 € i.v."
  email: "privacy@akaion.com", // default: casella privacy gestita da Akaion per il titolare
  telefono: "__TELEFONO__",
  whatsapp: "" as string, // es. "375 591 7703" se il negozio risponde su WhatsApp
  albo: "" as string, // professioni regolamentate (D.Lgs. 70/2003 art. 7), es. "Iscritto n. 109 all'Albo dei Fisioterapisti di …"
  sanitario: false, // true se prenotazioni/note possono contenere dati sulla salute (fisio, medici, psicologi)
  kaio: true, // prenotazioni/ordini/visite gestiti con Kaio
  vendita: null as null | "ritiro" | "spedizione", // ordini online: ritiro in negozio o spedizione
  ia: null as null | string, // es. "Alcune immagini del sito sono generate con intelligenza artificiale…"
  aggiornato: "__DATA__",
};

export const Route = createFileRoute("/privacy")({
  head: () => ({
    meta: [
      { title: `Privacy, cookie e note legali · ${L.titolare}` },
      { name: "description", content: `Informativa privacy e cookie del sito ${L.sito}.` },
    ],
  }),
  component: Privacy,
});

function S({ id, title, children }: { id?: string; title: string; children: ReactNode }) {
  return (
    <section id={id} className="mt-12 scroll-mt-24">
      <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
      <div className="mt-4 space-y-4 leading-relaxed opacity-85">{children}</div>
    </section>
  );
}

const a = "underline underline-offset-2";

// Email se c'è, altrimenti telefono.
function Contatto() {
  return L.email ? (
    <a className={a} href={`mailto:${L.email}`}>{L.email}</a>
  ) : (
    <a className={a} href={`tel:${L.telefono.replace(/\s/g, "")}`}>{L.telefono}</a>
  );
}

function Privacy() {
  const titolare = `${L.titolare}, ${L.sede}, P.IVA ${L.piva}`;
  return (
    <main className="mx-auto max-w-3xl px-6 pb-24 pt-28 md:pt-36">
      <Link to="/" className="text-sm opacity-70 hover:opacity-100">
        ← Torna al sito
      </Link>
      <h1 className="mt-6 text-4xl font-semibold tracking-tight md:text-6xl">Note legali</h1>
      <p className="mt-4 opacity-70">Aggiornate il {L.aggiornato}.</p>
      <nav className="mt-6 flex flex-wrap gap-x-5 gap-y-2 text-sm">
        <a className={a} href="#privacy">Privacy</a>
        <a className={a} href="#cookie">Cookie</a>
        {L.ia && <a className={a} href="#ia">Intelligenza artificiale</a>}
        {L.vendita && <a className={a} href="#vendita">Condizioni di vendita</a>}
      </nav>

      <S title="Chi gestisce il sito">
        <p>
          {titolare}
          {L.rea && ` · REA ${L.rea}`}
          {L.capitale && ` · Capitale sociale ${L.capitale}`}
          {L.albo && ` · ${L.albo}`}.
          <br />
          {L.email && (
            <>
              Email <Contatto /> ·{" "}
            </>
          )}
          Tel. <a className={a} href={`tel:${L.telefono.replace(/\s/g, "")}`}>{L.telefono}</a>
          {L.whatsapp && (
            <>
              {" "}· WhatsApp{" "}
              <a className={a} href={`https://wa.me/39${L.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer">
                {L.whatsapp}
              </a>
            </>
          )}
        </p>
      </S>

      <S id="privacy" title="Informativa privacy">
        <p>
          Questa informativa spiega, ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR),
          come trattiamo i dati personali di chi visita {L.sito} e di chi ci contatta.
        </p>
        <p>
          <b>Titolare del trattamento</b>: {titolare}, <Contatto />.
        </p>
        <p>
          <b>Dati di navigazione.</b> Il server che ospita il sito registra per motivi di sicurezza
          dati tecnici come indirizzo IP, browser e pagine richieste. Li conserva per pochi giorni e
          non li usa per identificarti (legittimo interesse alla sicurezza, art. 6.1.f GDPR).
        </p>
        {L.kaio && (
          <p>
            <b>Prenotazioni, ordini e richieste.</b> Se prenoti, ordini o ci scrivi dal sito ci dai
            nome, telefono, email ed eventuali note. Li usiamo solo per gestire la tua richiesta:
            conferma, promemoria, spostamenti, disdette
            {L.vendita ? ", preparazione dell'ordine" : ""} e pagamento (esecuzione di un
            contratto o di misure precontrattuali, art. 6.1.b GDPR), e per gli obblighi fiscali
            (art. 6.1.c). Ti mandiamo comunicazioni promozionali solo se ce lo chiedi. Fornire i
            dati è facoltativo, ma senza non possiamo gestire la richiesta.
          </p>
        )}
        {L.sanitario && (
          <p>
            <b>Dati sulla salute.</b> Le informazioni sul tuo stato di salute che ci dai (nelle note
            della prenotazione o durante la visita) le trattiamo solo per la prestazione sanitaria che
            chiedi, sotto il segreto professionale (art. 9.2.h GDPR e art. 2-septies D.Lgs. 196/2003).
            Ti consigliamo di non scrivere dettagli clinici nelle note: ne parliamo di persona.
          </p>
        )}
        <p>
          <b>Contatti diretti.</b> Se ci chiami, ci scrivi su WhatsApp o per email, usiamo i tuoi
          dati solo per risponderti. WhatsApp è un servizio di Meta Platforms, che tratta i dati
          secondo la propria informativa.
        </p>
        <p>
          <b>Chi tratta i dati per noi.</b> Il sito è ospitato da Vercel Inc. (USA, aderente al
          Data Privacy Framework UE-USA).
          {L.kaio && (
            <>
              {" "}
              Prenotazioni, ordini e statistiche di visita sono gestiti con Kaio di Akaion S.r.l.
              (Via Giovanni Spadolini 7, 20141 Milano), nominata responsabile del trattamento (art.
              28 GDPR); i suoi fornitori sono elencati nell'
              <a className={a} href="https://smallbusiness.akaion.com/legal/dpa" target="_blank" rel="noopener noreferrer">
                accordo sul trattamento dei dati
              </a>
              . I pagamenti online sono gestiti da Stripe: non vediamo i dati della tua carta.
            </>
          )}
          {L.vendita === "spedizione" &&
            " Per spedirti l'ordine passiamo nome, indirizzo e telefono al corriere scelto (BRT, GLS, SDA, Poste Italiane o altri) tramite Packlink (Packlink Shipping S.L., Spagna), solo per la consegna."}{" "}
          Quando un fornitore tratta dati fuori dallo Spazio economico europeo, il trasferimento si
          basa sul Data Privacy Framework UE-USA o sulle Clausole contrattuali standard della
          Commissione europea. Non vendiamo i tuoi dati e non li cediamo a terzi per pubblicità.
        </p>
        <p>
          <b>Per quanto tempo.</b> Per il tempo necessario a gestire la richiesta e il rapporto con
          te; i documenti fiscali per 10 anni come previsto dalla legge (art. 2220 c.c.).
        </p>
        <p>
          <b>I tuoi diritti.</b> Puoi chiedere in ogni momento accesso, rettifica, cancellazione,
          limitazione, portabilità dei dati e opporti al trattamento (artt. 15–22 GDPR) scrivendo a{" "}
          <Contatto />. Puoi anche presentare reclamo
          al Garante per la protezione dei dati personali (
          <a className={a} href="https://www.garanteprivacy.it" target="_blank" rel="noopener noreferrer">
            garanteprivacy.it
          </a>
          ). Non prendiamo decisioni automatizzate né facciamo profilazione.
        </p>
      </S>

      <S id="cookie" title="Cookie">
        <p>
          Questo sito non usa cookie e non salva nulla nel tuo browser: niente cookie di
          profilazione, niente statistiche di terze parti, niente pixel pubblicitari. I caratteri
          tipografici sono caricati dal nostro server, non da Google.
          {L.kaio &&
            " Le visite sono contate da Kaio senza cookie e senza identificarti: solo il numero di pagine viste e di tocchi su Chiama, WhatsApp e Prenota."}{" "}
          Per questo non ti chiediamo alcun consenso (Linee guida del Garante sui cookie del 10
          giugno 2021).
        </p>
        <p>
          I link a servizi esterni (Google Maps, Instagram, Facebook, WhatsApp) si aprono sui loro
          siti, dove valgono le loro informative e i loro cookie.
        </p>
      </S>

      {L.ia && (
        <S id="ia" title="Uso dell'intelligenza artificiale">
          <p>
            Informativa ai sensi dell'art. 50 del Regolamento (UE) 2024/1689 (AI Act) e della
            Legge 132/2025. {L.ia}
          </p>
          <p>Tutto quello che pubblichiamo lo controlliamo noi prima che vada online. Il sito non usa chatbot né sistemi di IA che dialogano con te.</p>
        </S>
      )}

      {L.vendita && (
        <S id="vendita" title="Condizioni di vendita">
          <p>
            Venditore: {titolare}. I prezzi sono in euro, IVA inclusa. L'ordine è confermato quando
            ricevi la conferma; se un prodotto non è disponibile ti avvisiamo e, se hai già pagato,
            ti rimborsiamo per intero.
          </p>
          {L.vendita === "ritiro" ? (
            <p>
              Gli ordini si ritirano in negozio nella fascia scelta. Paghi online o al ritiro,
              come indicato al momento dell'ordine. Per i prodotti freschi e deperibili o
              preparati su richiesta il diritto di recesso è escluso (art. 59, lett. c e d, Codice
              del Consumo); per gli altri prodotti puoi recedere entro 14 giorni dal ritiro
              scrivendo a <Contatto /> e riportando il
              prodotto integro.
            </p>
          ) : (
            <p>
              Spese e tempi di consegna sono indicati prima del pagamento. Se sei un consumatore
              puoi recedere entro 14 giorni dalla consegna senza dare motivazioni (artt. 52 e
              seguenti del Codice del Consumo, D.Lgs. 206/2005), scrivendo a{" "}
              <Contatto />; rimandi il prodotto
              integro entro altri 14 giorni a tue spese e ti rimborsiamo entro 14 giorni dal
              recesso con lo stesso mezzo di pagamento. Sono esclusi i prodotti personalizzati o
              fatti su misura (art. 59, lett. c).
            </p>
          )}
          <p>
            <b>Come recedere.</b> Basta una dichiarazione esplicita, anche con questo modulo
            (Allegato I, parte B, Codice del Consumo): «Destinatario: {titolare}, <Contatto />.
            Con la presente notifico il recesso dal mio contratto di vendita dei seguenti beni:
            … · Ordinato il / ricevuto il … · Nome e indirizzo … · Data».
          </p>
          <p>
            Sui prodotti vale la garanzia legale di conformità di 24 mesi (artt. 128 e seguenti
            del Codice del Consumo). Per qualsiasi problema scrivici: rispondiamo entro 2 giorni
            lavorativi. Il contratto è regolato dalla legge italiana; per il consumatore resta
            competente il foro del suo luogo di residenza.
          </p>
        </S>
      )}
    </main>
  );
}
