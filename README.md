# matgato · M / Sketchbook

Sito portfolio di Matteo — **https://matgato.malaccessories.com**
Ospitato su Netlify (progetto `bespoke-speculoos-15f759`). Dominio su Register.it, record CNAME `matgato` → `bespoke-speculoos-15f759.netlify.app` (non toccarlo).

## Struttura

```
site/                 ← il sito vero e proprio: questo è ciò che va online
  index.html          ← tutta la pagina (testi, sezioni, stile, script)
  images/             ← immagini in WebP (sk-xxx = schizzo, xxx = forma finita)
  video/              ← animazione dell'apertura (hero.webm + hero.mp4)
  fonts/              ← Cormorant Garamond e Inter, ospitati sul sito
  og-image.jpg        ← anteprima quando condividi il link
  sitemap.xml, robots.txt, favicon…
tools/pairs.py        ← aggiunge / toglie coppie Sketch → Form
netlify.toml          ← impostazioni Netlify (cache)
.vscode/tasks.json    ← comandi pronti in VS Code
CLAUDE.md             ← istruzioni per Claude, se lo usi in VS Code
```

## Prima volta (una sola volta)

1. Apri `matgato.code-workspace` con VS Code.
2. Installa le estensioni consigliate quando VS Code te lo propone (Live Server).
3. **Terminal → Run Task… → Setup · Installa Pillow** (serve per convertire le immagini).
4. Installa Node.js da https://nodejs.org (versione LTS), poi **Run Task… → Setup · Collega Netlify**: si apre il browser, accedi a Netlify e il workspace viene collegato al progetto esistente.

## Uso quotidiano

Tutti i comandi sono in **Terminal → Run Task…** (oppure `Cmd+Shift+P` → "Run Task").

| Cosa vuoi fare | Comando |
|---|---|
| Vedere il sito in locale | **1 · Anteprima sito**, poi apri http://localhost:5173 (oppure clic destro su `site/index.html` → *Open with Live Server*) |
| Pubblicare online | **2 · Pubblica su Netlify** |
| Vedere l'elenco delle coppie | **Coppie · Elenco** |
| Aggiungere una coppia | **Coppie · Aggiungi** (o *Aggiungi (larga)*) e rispondi alle domande |
| Togliere una coppia | **Coppie · Rimuovi** e scrivi l'id |

### Aggiungere una coppia schizzo → forma

Run Task → **Coppie · Aggiungi**, poi:
- **ID**: una parola senza spazi (es. `verum`)
- **Titolo**: es. `Verum`
- **Percorso schizzo / immagine finita**: trascina il file dal Finder dentro la casella e premi Invio
- **Frase**: il testo sotto la coppia

Lo script converte le immagini, aggiunge la coppia in fondo, rinumera tutte le coppie, aggiorna contatori e sitemap. Se le coppie a metà larghezza diventano dispari ti avvisa: in quel caso aggiungine un'altra o usa *Aggiungi (larga)*.

Per inserirla in un punto preciso usa il terminale:
```
python3 tools/pairs.py add --id nome --title "Nome" --sketch ~/Desktop/a.jpg --form ~/Desktop/b.jpg --caption "Frase." --before millennium
```

### Modificare testi
Apri `site/index.html`, cerca il testo con `Cmd+F`, modificalo, salva. Controlla in anteprima e pubblica.

## Pubblicare senza VS Code
Va sempre bene anche il vecchio metodo: trascina la cartella **site** su Netlify → Deploys.
Per tornare a una versione precedente: Netlify → Deploys → clic sulla versione → **Publish deploy**.

## Statistiche e cookie
- Google Tag Manager `GTM-M3FMTQSJ` si carica **solo dopo "Accetta"** nel banner (Consent Mode v2).
- GA4 si configura dentro Tag Manager (Google tag → trigger *Initialization – All Pages*).
