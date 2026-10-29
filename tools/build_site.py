"""Stage 4: join the White and Black runs into the home page.
Run from the repo root after both:  SIDE=white ... ; SIDE=black ...   then   python tools/build_site.py"""
import os, json, sys
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = common.PLAYER; FULL = common.FULL_NAME

def read(side, name):
    return open(os.path.join(ROOT, "build", side, name), encoding="utf-8").read()

def front(title, menu, weight, menu_on=True):
    return f'---\ntitle: "{title}"\nheader_menu_title: "{menu}"\nnavigation_menu_title: "{menu}"\nweight: {weight}\nheader_menu: {"true" if menu_on else "false"}\n---\n'



def main():
    ch = os.path.join(ROOT, "content", "en", "homepage"); os.makedirs(ch, exist_ok=True)
    for f in os.listdir(ch):
        if f.endswith(".md"): os.remove(os.path.join(ch, f))
    open(os.path.join(ch, "index.md"), "w").write("---\nheadless: true\n---\n")
    st = {s: json.load(open(os.path.join(ROOT, "build", s, "stats.json"))) for s in ("white", "black")}
    tw, tb = st["white"]["total"], st["black"]["total"]
    n = tw["n"]; sc = tw["score"]
    meta = json.load(open(os.path.join(ROOT, "build", "meta.json")))
    def pct(x): return f"{x:.0%}"
    ov = (f"What {n:,} titled players actually played in **{meta['event']}** ({meta['date']}). "
          f"White scored **{pct(sc)}** (+{tw['w']} ={tw['d']} −{tw['l']}); {pct(tw['d']/n)} of the games were drawn. "
          f"Average rating {meta['avg_elo']}, from {meta['min_elo']} to {meta['max_elo']}. "
          "Every game appears twice: once on the White side (scored for White) and once on the Black side (scored for Black).\n\n")
    rows = "| First move | Games | Share | White scores |\n| --- | --- | --- | --- |\n"
    for lbl, w in st["white"]["first"].items():
        rows += f"| {lbl} | {w['n']} | {pct(w['n']/n)} | {pct(w['score'])} |\n"
    ov += rows + "\n"
    ov += (f"## What White plays\n\n[![What White played, the big picture](white/trees/big-picture/preview.jpg)](white/trees/big-picture/)\n\n- [See White's openings and lines](#white)\n\n"
           f"## What Black plays\n\n[![What Black played, the big picture](black/trees/big-picture/preview.jpg)](black/trees/big-picture/)\n\n- [See Black's replies and lines](#black)\n")
    open(os.path.join(ch, "01-overview.md"), "w", encoding="utf-8").write(front("Overview", "Overview", 1) + ov)
    open(os.path.join(ch, "02-white.md"), "w", encoding="utf-8").write(front("What White plays", "White", 2) + read("white", "section.md"))
    open(os.path.join(ch, "03-black.md"), "w", encoding="utf-8").write(front("What Black plays", "Black", 3) + read("black", "section.md"))
    open(os.path.join(ch, "05-how.md"), "w", encoding="utf-8").write(
        front("How This Is Made", "How It Works", 5, menu_on=False) +
        f"The games come from the PGN file `data/ttc.pgn` ({n:,} games with moves).\n\n"
        "Every game is replayed move by move and added to one tree per colour, counting how many games pass through each position and how that colour scored.\n\n"
        "To analyse a new tournament: replace `data/ttc.pgn` with the new PGN, run `./build.sh`, and push.\n\n"
        "## Tools\n"
        "- [python-chess](https://github.com/niklasf/python-chess) reads the games and draws the boards\n"
        "- [Graphviz](https://graphviz.org/) lays out the branches\n"
        "- [Lichess opening names](https://github.com/lichess-org/chess-openings) (CC0) give each game its opening name\n"
        "- [chess.js](https://github.com/jhlywa/chess.js) replays the games in your browser\n"
        "- [Hugo](https://gohugo.io/) builds the site\n")
    # cover image: assets/images/header-*.jpg is a chosen photo (used by content/en/_index.md); the tree crop below is only a fallback
    src = os.path.join(ROOT, "build", "white", "big-picture.png")
    if os.path.exists(src) and not any(f.startswith("header-") for f in os.listdir(os.path.join(ROOT, "assets", "images"))):
        im = Image.open(src).convert("RGB"); W, H = im.size
        cw = min(W, 2400); chh = int(cw * 1338 / 2400); x0 = max(0, (W - cw) // 2)
        crop = im.crop((x0, 0, x0 + cw, min(H, chh))).resize((2400, 1338))
        out = Image.blend(crop.filter(ImageFilter.GaussianBlur(9)), Image.new("RGB", crop.size, (20, 35, 50)), 0.86)
        os.makedirs(os.path.join(ROOT, "assets", "images"), exist_ok=True)
        out.save(os.path.join(ROOT, "assets", "images", "cover-image.jpg"), quality=80, optimize=True)
    print("site content written")

if __name__ == "__main__":
    main()
