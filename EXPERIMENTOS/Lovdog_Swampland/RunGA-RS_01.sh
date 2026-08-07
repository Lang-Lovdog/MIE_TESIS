#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "GA_GRID" -c "$(pwd)" -l default -- toilet "GA RANDOM SEARCH"
  zellij ac go-to-tab-name "GA_RS"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_ga_random_search 16 &
else
  echo "No ZELLIJ session"
fi

