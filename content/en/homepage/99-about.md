---
title: "About"
header_menu_title: "About"
navigation_menu_title: "About"
weight: 99
header_menu: true
---
**What Ya Playing?** is for looking at the openings that were played at the Titled Tuesday. Each Titled Tuesday Blitz is one tournament tab under the title: pick a tournament, then look at what White played and what Black replied.

## What you can see
- the most popular first moves, openings, variations and lines, with how often each was played and how it scored
- a tree of the whole field for White and for Black, then a tree for each first move, then every game in each line
- every game replayed on a live board, with the players and their ratings

## New tournaments
Every time there is a new Titled Tuesday, it is added as another tab (named TTC_MMDDYY, for example TTC_102726 is October 27, 2026). The newest tournament opens first.

## How it is made
Every game is replayed move by move and added to one tree per colour, counting how many games pass through each position and how that colour scored. Every game appears on both sides: on the White side it is scored for White, on the Black side for Black.

- [python-chess](https://github.com/niklasf/python-chess) reads the games and draws the boards
- [Graphviz](https://graphviz.org/) lays out the branches
- [Lichess opening names](https://github.com/lichess-org/chess-openings) (CC0) give each game its opening name
- [chess.js](https://github.com/jhlywa/chess.js) replays the games in your browser
- [Hugo](https://gohugo.io/) builds the site
