#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "GA_GRID" -c "$(pwd)" -l default -- toilet "GA GRID"
  zellij ac go-to-tab-name "GA_GRID"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_ga_grid 0  4  8 12 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_ga_grid 1  5  9 13 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_ga_grid 2  6 10 14 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_ga_grid 3  7 11 15 &
else
  echo "No ZELLIJ session"
fi

