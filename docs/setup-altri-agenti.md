# Cursor, Codex, altri agenti

Il bundle non dipende da Claude: è uno script Python e una procedura scritta. Qualunque agente che legga file e lanci comandi può farlo.

## La procedura in una pagina

`AGENTS.md` nella radice del repo è la versione corta, pensata per essere letta da un agente. `skills/kaio-bundle/SKILL.md` è quella completa. Dagliele da leggere, poi:

> Leggi AGENTS.md di kaio-bundle e installa il bundle su questo sito, slug `<slug>`, dominio `<https://…>`.

## Cursor

1. Scarica il repo accanto al sito: `git clone https://github.com/akaion-ai/kaio-bundle.git`.
2. In Cursor, impostazioni → **Rules** → aggiungi una regola di progetto che punta a `kaio-bundle/AGENTS.md` (o copia il testo).
3. MCP Akaion: impostazioni → **MCP** → aggiungi server con questo JSON:

```json
{
  "mcpServers": {
    "akaion": { "url": "https://api.website.prod.akaion.com/mcp" }
  }
}
```

Al primo uso Cursor apre il login OAuth di Akaion.

## Codex (OpenAI)

```sh
codex mcp add akaion --url https://api.website.prod.akaion.com/mcp
```

Poi nella chat di Codex: «leggi kaio-bundle/AGENTS.md e procedi».

## Senza nessun agente

```sh
python3 kaio-bundle/bundle_install.py <cartella sito> <slug>
```

e segui i DA FARE a mano. La configurazione su Kaio si fa dal pannello: https://smallbusiness.akaion.com/admin (staff) con gli stessi passi del `SKILL.md`, sezione 1.
