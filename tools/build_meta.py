"""Reads the PGN header data used by the overview: event, date, rating range. Run from the repo root."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common, chess.pgn
ev, dates, elos = "", [], []
with open(os.path.join(common.DATA, common.PGN_FILE), encoding="utf-8", errors="replace") as f:
    while (h := chess.pgn.read_headers(f)) is not None:
        ev = ev or h.get("Event", "")
        dates.append(h.get("Date", ""))
        for k in ("WhiteElo", "BlackElo"):
            if h.get(k, "").isdigit(): elos.append(int(h[k]))
name = re.sub(r"[-_]+", " ", ev).strip() or "this tournament"
OUTD = os.path.join(common.HERE, "..", "build", common.EVENT); os.makedirs(OUTD, exist_ok=True)
d = sorted(x for x in dates if x and "?" not in x)
json.dump(dict(id=common.EVENT, label=common.EVENT_LABEL, event=name, date=(d[0].replace(".", "-") if d else ""), avg_elo=round(sum(elos) / len(elos)) if elos else 0,
               min_elo=min(elos, default=0), max_elo=max(elos, default=0)), open(os.path.join(OUTD, "meta.json"), "w"))
