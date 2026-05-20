#!/bin/bash

export -f run_da_grid

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "PSO_GRID" -c "$(pwd)" -l default -- toilet "PSO GRID"
  zellij ac go-to-tab-name "PSO_GRID"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 0 4  8 12 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 1 5  9 13 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 2 6 10 14 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_grid 3 7 11 15 &
else
  echo "No ZELLIJ session"
fi


#  python ./LovdogSwamplandMain2.py PSO 0 4  8 12 &
#  python ./LovdogSwamplandMain2.py PSO 1 5  9 13 &
#  python ./LovdogSwamplandMain2.py PSO 2 6 10 14 &
#  python ./LovdogSwamplandMain2.py PSO 3 7 11 15 &
