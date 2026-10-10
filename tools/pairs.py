#!/usr/bin/env python3
"""
Gestione delle coppie Sketch → Form del sito matgato.

Esempi (dalla cartella del workspace):
  python3 tools/pairs.py list
  python3 tools/pairs.py add --id nuovo --title "Nuovo" --sketch ~/Desktop/schizzo.jpg --form ~/Desktop/finito.jpg --caption "Testo sotto la coppia."
  python3 tools/pairs.py add ... --wide          (coppia a tutta larghezza)
  python3 tools/pairs.py add ... --before millennium   (inserisce prima di un'altra coppia)
  python3 tools/pairs.py remove --id nuovo
  python3 tools/pairs.py refresh                 (riallinea numeri, contatori e sitemap)

Le immagini vengono ridimensionate (max 1600 px) e salvate in WebP in site/images/.
"""
import argparse, datetime, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
INDEX = os.path.join(SITE, "index.html")
IMAGES = os.path.join(SITE, "images")
URL = "https://matgato.malaccessories.com/"

PAIR_RE = re.compile(r'          <div class="pair(?: wide)? fade-up">\n.*?\n          </div>\n', re.S)


def load():
    with open(INDEX, encoding="utf-8") as f:
        return f.read()


def save(s):
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(s)


def pairs_block(s):
    start = s.index('<div class="pairs">') + len('<div class="pairs">\n')
    end = s.index("        </div>\n      </section>", start)
    return start, end


def list_pairs(s):
    a, b = pairs_block(s)
    out = []
    for m in PAIR_RE.finditer(s, a, b):
        blk = m.group(0)
        pid = re.search(r'id="flip-([\w-]+)"', blk).group(1)
        title = re.search(r'</span>([^<]+)</h3>', blk).group(1)
        out.append((pid, title, "wide" in blk.split("\n")[0], m.start(), m.end()))
    return out


def to_webp(src, name):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("Manca Pillow. Installalo con:  python3 -m pip install Pillow")
    im = ImageOps.exif_transpose(Image.open(os.path.expanduser(src))).convert("RGB")
    im.thumbnail((1600, 1600))
    dst = os.path.join(IMAGES, name + ".webp")
    im.save(dst, "WEBP", quality=80, method=6)
    print("  immagine:", os.path.relpath(dst, ROOT), im.size)


def refresh(s):
    # numerazione 01, 02, ...
    a, b = pairs_block(s)
    block = s[a:b]
    n = [0]

    def num(m):
        n[0] += 1
        return f'<span class="n">{n[0]:02d}</span>'

    block = re.sub(r'<span class="n">\d+</span>', num, block)
    s = s[:a] + block + s[b:]
    total = n[0]
    s = re.sub(r'Sketch → Form<span class="count">\d+</span>', f'Sketch → Form<span class="count">{total}</span>', s)
    s = re.sub(r'\d+ passaggi dallo schizzo', f'{total} passaggi dallo schizzo', s)
    imgs = sorted(set(re.findall(r'images/([\w-]+)\.webp', s)))
    s = re.sub(r'<span>\d+ tavole</span>', f'<span>{len(imgs)} tavole</span>', s)
    # sitemap
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
          f'<url><loc>{URL}</loc><lastmod>{today}</lastmod>']
    sm += [f'<image:image><image:loc>{URL}images/{i}.webp</image:loc></image:image>' for i in imgs]
    sm += ['</url>', '</urlset>', '']
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))
    halves = sum(1 for p in list_pairs(s) if not p[2])
    print(f"  coppie: {total} · tavole: {len(imgs)} · sitemap aggiornata")
    if halves % 2:
        print("  ATTENZIONE: le coppie a metà larghezza sono dispari, l'ultima resta da sola.\n"
              "  Rendi una coppia larga (--wide) oppure aggiungine un'altra.")
    return s


def block_for(pid, title, sketch_alt, form_alt, caption, wide, ratio):
    t = html.escape(title, quote=True)
    style = f' style="aspect-ratio:{ratio}"' if ratio else ""
    return f'''          <div class="pair{' wide' if wide else ''} fade-up">
            <div class="compare" tabindex="0"{style}>
              <input type="checkbox" class="flip" id="flip-{pid}" aria-label="Mostra la forma finita">
              <img class="before" src="images/sk-{pid}.webp" alt="Schizzo: {html.escape(sketch_alt, quote=True)}" loading="lazy">
              <img class="after" src="images/{pid}.webp" alt="Forma finita: {html.escape(form_alt, quote=True)}" loading="lazy">
              <span class="tag l">Sketch</span><span class="tag r">Form</span>
              <input type="range" id="cmp-{pid}" min="0" max="100" value="50" aria-label="Confronta schizzo e forma: {t}">
              <span class="handle"></span>
              <label for="flip-{pid}" class="hit"><span>Tocca</span></label>
            </div>
            <div class="pair-cap"><h3><span class="n">00</span>{html.escape(title)}</h3><p>{html.escape(caption)}</p></div>
          </div>
'''


def main():
    ap = argparse.ArgumentParser(description="Coppie Sketch → Form")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("refresh")
    a = sub.add_parser("add")
    a.add_argument("--id", required=True, help="nome breve senza spazi, es. verum")
    a.add_argument("--title", required=True)
    a.add_argument("--sketch", required=True, help="percorso dell'immagine dello schizzo")
    a.add_argument("--form", required=True, help="percorso dell'immagine finita")
    a.add_argument("--caption", required=True)
    a.add_argument("--alt", default=None, help="descrizione breve del soggetto per l'accessibilità")
    a.add_argument("--wide", action="store_true")
    a.add_argument("--ratio", default=None, help="proporzioni per coppie larghe, es. 5/4")
    a.add_argument("--before", default=None, help="id della coppia prima della quale inserirla")
    r = sub.add_parser("remove")
    r.add_argument("--id", required=True)
    r.add_argument("--keep-images", action="store_true")
    args = ap.parse_args()

    s = load()
    if args.cmd == "list":
        for i, (pid, title, wide, *_) in enumerate(list_pairs(s), 1):
            print(f"{i:02d}  {pid:<14} {title}{'  (larga)' if wide else ''}")
        return
    if args.cmd == "refresh":
        save(refresh(s)); return
    if args.cmd == "add":
        pid = re.sub(r"[^a-z0-9-]", "-", args.id.lower()).strip("-")
        if any(p[0] == pid for p in list_pairs(s)):
            sys.exit(f"Esiste già una coppia con id '{pid}'.")
        to_webp(args.sketch, "sk-" + pid)
        to_webp(args.form, pid)
        alt = args.alt or args.title
        blk = block_for(pid, args.title, alt, alt, args.caption, args.wide, args.ratio)
        if args.before:
            target = next((p for p in list_pairs(s) if p[0] == args.before), None)
            if not target:
                sys.exit(f"Coppia '{args.before}' non trovata.")
            pos = target[3]
        else:
            pos = pairs_block(s)[1]
            blk = "\n" + blk
        s = s[:pos] + blk + ("\n" if args.before else "") + s[pos:]
        print(f"Aggiunta coppia '{args.title}'.")
        save(refresh(s)); return
    if args.cmd == "remove":
        target = next((p for p in list_pairs(s) if p[0] == args.id), None)
        if not target:
            sys.exit(f"Coppia '{args.id}' non trovata.")
        s = s[:target[3]] + s[target[4]:]
        s = re.sub(r"\n{3,}(          <div class=\"pair)", r"\n\n\1", s)
        if not args.keep_images:
            for n in ("sk-" + args.id, args.id):
                p = os.path.join(IMAGES, n + ".webp")
                if os.path.exists(p) and f"images/{n}.webp" not in s:
                    os.remove(p); print("  rimossa", os.path.relpath(p, ROOT))
        print(f"Rimossa coppia '{args.id}'.")
        save(refresh(s)); return


if __name__ == "__main__":
    main()
