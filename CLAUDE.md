# CLAUDE.md — matgato · M / Sketchbook

Portfolio statico di Matteo (art director / graphic designer). Online su https://matgato.malaccessories.com, hosting Netlify (progetto `bespoke-speculoos-15f759`), DNS su Register.it con CNAME `matgato`. Chi lo gestisce è Laura: rispondi in italiano, semplice e operativo.

## Come è fatto
- Tutto il sito è **un solo file**: `site/index.html` (HTML + CSS + JS inline). Nessun framework, nessun build step: ciò che c'è in `site/` va online così com'è.
- Immagini in `site/images/*.webp` (max 1600 px, qualità 80). Convenzione coppie: `sk-<id>.webp` = schizzo, `<id>.webp` = forma finita.
- Font self-hosted in `site/fonts/` (Cormorant Garamond per titoli, Inter per testo). Non reintrodurre Google Fonts (GDPR).
- Palette: fondo `#090a0b`, pannello `#151719`, testo `#f3f0ea`, accento oro `#b99661`. Tema unico scuro.
- Apertura con video `site/video/hero.webm|mp4` (Artlist, loop 4 s); si disattiva con risparmio dati o prefers-reduced-motion.

## Sezioni (in ordine)
Hero → barra sezioni sticky (con "M" e pulsante Contatti) → **01 Sketch → Form** (coppie con confronto) → **02 Subject** (digital print, etichetta "3D · Digital print", il ritratto verde è solo "Digital print") → The skull → **03 On the table** → interludio → M → **04 Contatti** (info@malaccessories.com) → footer.
La galleria "Sketches" e l'interludio "Guardare non è la stessa cosa che vedere" sono stati tolti di proposito: non rimetterli.

## Coppie Sketch → Form
- Usa sempre `python3 tools/pairs.py` (list / add / remove / refresh): rinumera, aggiorna contatori "Sketch → Form N", "N tavole", meta description e `sitemap.xml`.
- Le coppie a metà larghezza devono essere **in numero pari**; quelle larghe (`pair wide`) occupano una riga. Millennium è larga con `aspect-ratio:5/4` e chiude la sezione.
- Il confronto deve funzionare anche **senza JavaScript** (checkbox + label "Tocca") e su iPhone: non rimuovere `.flip`, `.hit`, né i listener touch.
- Le didascalie scritte da Claude vanno segnalate a Laura come "da far rivedere a Matteo".

## Regole
- Niente pulsante Etsy nel sito.
- Analytics: GTM `GTM-M3FMTQSJ` caricato solo dopo consenso (banner `#consent`, localStorage `mg-consent`). Non aggiungere il `<noscript>` di GTM.
- Non toccare il DNS su Register.it e non creare il sottodominio dal pannello hosting di Register (romperebbe il CNAME).
- Dopo ogni modifica: anteprima con `python3 -m http.server 5173 --directory site`, poi `npx netlify-cli deploy --prod --dir=site`.
- Controlla sempre la resa a 390 px di larghezza (iPhone) e che la pagina non scorra in orizzontale.
