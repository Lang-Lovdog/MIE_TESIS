#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "PSO_GRID" -c "$(pwd)" -l default -- toilet "PSO GRID"
  zellij ac go-to-tab-name "PSO_GRID"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 12 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 13 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 14 &
#  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 0 4  8 12 &
#  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 1 5  9 13 &
#  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 2 6 10 14 &
#  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 3 7 11 15 &
else
  echo "No ZELLIJ session"
fi
