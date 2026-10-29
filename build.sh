#!/bin/bash
# Rebuild everything from data/ttc.pgn:  ./build.sh   (then: hugo server, or commit + push to deploy)
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:-/home/claude/tools/py}"
mkdir -p build
python3 tools/build_meta.py
for S in white black; do
  export SIDE=$S
  mkdir -p build/$S
  python3 tools/build_trees.py > build/$S/trees.log 2>&1
  python3 tools/build_variations.py > build/$S/variations.log 2>&1
  python3 tools/build_pages.py > build/$S/pages.log 2>&1
  touch build/$S.done
done
python3 tools/build_site.py > build/site.log 2>&1
touch build/ALL_DONE
