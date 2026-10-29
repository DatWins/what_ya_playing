#!/bin/bash
# One tab per tournament PGN in data/ (name them TTC_102726.pgn, TTC_110326.pgn, ...).
#   ./build.sh                    rebuild every PGN
#   ./build.sh TTC_110326.pgn     build only the new one (the older tabs are kept in eventdata/)
# Then commit and push; GitHub Actions publishes the site.
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:-/home/claude/tools/py}"
mkdir -p build eventdata
FILES=("$@"); [ ${#FILES[@]} -eq 0 ] && FILES=($(cd data && ls *.pgn))
for F in "${FILES[@]}"; do
  F=$(basename "$F"); export EVENT_PGN="$F"; EV=$(echo "${F%.pgn}" | tr 'A-Z' 'a-z')
  rm -rf "static/$EV" "build/$EV"; mkdir -p "build/$EV" "eventdata/$EV"
  python3 tools/build_meta.py
  for S in white black; do
    export SIDE=$S
    mkdir -p build/$EV/$S eventdata/$EV/$S
    python3 tools/build_trees.py > build/$EV/$S/trees.log 2>&1
    python3 tools/build_variations.py > build/$EV/$S/variations.log 2>&1
    python3 tools/build_pages.py > build/$EV/$S/pages.log 2>&1
    cp build/$EV/$S/section.md build/$EV/$S/stats.json eventdata/$EV/$S/
  done
  cp build/$EV/meta.json eventdata/$EV/
done
unset SIDE EVENT_PGN
python3 tools/build_site.py > build/site.log 2>&1
touch build/ALL_DONE
