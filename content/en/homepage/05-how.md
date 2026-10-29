---
title: "How This Is Made"
header_menu_title: "How It Works"
navigation_menu_title: "How It Works"
weight: 5
header_menu: false
---
The games come from the PGN file `data/ttc.pgn` (2,230 games with moves).

Every game is replayed move by move and added to one tree per colour, counting how many games pass through each position and how that colour scored.

To analyse a new tournament: replace `data/ttc.pgn` with the new PGN, run `./build.sh`, and push.

## Tools
- [python-chess](https://github.com/niklasf/python-chess) reads the games and draws the boards
- [Graphviz](https://graphviz.org/) lays out the branches
- [Lichess opening names](https://github.com/lichess-org/chess-openings) (CC0) give each game its opening name
- [chess.js](https://github.com/jhlywa/chess.js) replays the games in your browser
- [Hugo](https://gohugo.io/) builds the site
