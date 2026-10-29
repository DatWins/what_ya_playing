# What Ya Playing?

What the field plays in a tournament: for White and for Black, the first moves, openings, variations and most popular lines, with the full games.
Current data: Chess.com Titled Tuesday Blitz, October 27, 2026 (2,230 games with moves); also TTC_101326 (October 13, 2026).

## Analyse a new tournament
1. Save the new PGN in `data/` as `TTC_MMDDYY.pgn` (the file name becomes the tab name). Each PGN is one tab.
2. Run `./build.sh TTC_MMDDYY.pgn` (builds just that tournament; `./build.sh` alone rebuilds all). Needs python-chess, Graphviz, CairoSVG, Pillow.
3. Commit and push. GitHub Actions builds the site with Hugo and publishes it to Pages (Settings → Pages → Source: GitHub Actions).

Opening names come from the [Lichess opening list](https://github.com/lichess-org/chess-openings) (CC0).
Every game appears on both sides: the White side is scored for White, the Black side for Black.
Tweak the thresholds in `tools/common.py` (`MIN_REPLY`, `SPLIT_OVER`) for bigger or smaller fields.
