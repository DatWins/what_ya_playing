"""Joins every event in eventdata/ into the home page: one tab per tournament (the tab bar is in layouts/partials/custom_head.html).
Run from the repo root after build.sh has filled eventdata/ :  python tools/build_site.py"""
import os, json, shutil
from PIL import Image, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ED = os.path.join(ROOT, "eventdata")

def front(title, menu, weight, menu_on=True):
    return f'---\ntitle: "{title}"\nheader_menu_title: "{menu}"\nnavigation_menu_title: "{menu}"\nweight: {weight}\nheader_menu: {"true" if menu_on else "false"}\n---\n'

def pct(x): return f"{x:.0%}"

def main():
    ch = os.path.join(ROOT, "content", "en", "homepage"); os.makedirs(ch, exist_ok=True)
    for f in os.listdir(ch):
        if f.endswith(".md"): os.remove(os.path.join(ch, f))
    open(os.path.join(ch, "index.md"), "w").write("---\nheadless: true\n---\n")
    events = []
    for ev in sorted(os.listdir(ED)):
        mp = os.path.join(ED, ev, "meta.json")
        if os.path.exists(mp): events.append(json.load(open(mp)))
    events.sort(key=lambda m: (m["date"], m["id"]), reverse=True)      # newest first
    weight = 1
    for m in events:
        ev, label = m["id"], m["label"]
        st = {s: json.load(open(os.path.join(ED, ev, s, "stats.json"))) for s in ("white", "black")}
        sec = {s: open(os.path.join(ED, ev, s, "section.md"), encoding="utf-8").read() for s in ("white", "black")}
        tw = st["white"]["total"]; n = tw["n"]
        ov = (f"**{label}**: what {n:,} games of **{m['event']}** ({m['date']}) looked like. "
              f"White scored **{pct(tw['score'])}** (+{tw['w']} ={tw['d']} −{tw['l']}); {pct(tw['d']/n)} of the games were drawn. "
              f"Average rating {m['avg_elo']}, from {m['min_elo']} to {m['max_elo']}. "
              "Every game appears twice: once on the White side (scored for White) and once on the Black side (scored for Black).\n\n"
              "| First move | Games | Share | White scores |\n| --- | --- | --- | --- |\n")
        for lbl, w in st["white"]["first"].items():
            ov += f"| {lbl} | {w['n']} | {pct(w['n']/n)} | {pct(w['score'])} |\n"
        ov += (f"\n## What White plays\n\n[![What White played, the big picture]({ev}/white/trees/big-picture/preview.jpg)]({ev}/white/trees/big-picture/)\n\n- [See White's openings and lines](#{ev}-white)\n\n"
               f"## What Black plays\n\n[![What Black played, the big picture]({ev}/black/trees/big-picture/preview.jpg)]({ev}/black/trees/big-picture/)\n\n- [See Black's replies and lines](#{ev}-black)\n")
        for part, title, body in (("overview", f"{label} · Overview", ov), ("white", f"{label} · What White plays", sec["white"]), ("black", f"{label} · What Black plays", sec["black"])):
            open(os.path.join(ch, f"{weight:02d}-{ev}-{part}.md"), "w", encoding="utf-8").write(front(title, f"{ev}-{part}", weight) + body)
            weight += 1
    open(os.path.join(ch, "99-how.md"), "w", encoding="utf-8").write(
        front("How This Is Made", "how-it-works", 99, menu_on=False) +
        "Each tournament PGN in `data/` becomes one tab. To add a new Titled Tuesday, save its PGN as `data/TTC_MMDDYY.pgn`, run `./build.sh TTC_MMDDYY.pgn` and push.\n\n"
        "Every game is replayed move by move and added to one tree per colour, counting how many games pass through each position and how that colour scored.\n\n"
        "## Tools\n"
        "- [python-chess](https://github.com/niklasf/python-chess) reads the games and draws the boards\n"
        "- [Graphviz](https://graphviz.org/) lays out the branches\n"
        "- [Lichess opening names](https://github.com/lichess-org/chess-openings) (CC0) give each game its opening name\n"
        "- [chess.js](https://github.com/jhlywa/chess.js) replays the games in your browser\n"
        "- [Hugo](https://gohugo.io/) builds the site\n")
    lst = [{k: m[k] for k in ("id", "label", "date")} for m in events]
    open(os.path.join(ROOT, "layouts", "partials", "events_data.html"), "w").write("window.EVENTS = " + json.dumps(lst) + ";")
    print("site content written:", [m["id"] for m in events])

if __name__ == "__main__":
    main()
