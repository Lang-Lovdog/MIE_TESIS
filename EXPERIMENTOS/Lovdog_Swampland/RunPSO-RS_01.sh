#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "PSO_GRID" -c "$(pwd)" -l default -- toilet "PSO RANDOM SEARCH"
  zellij ac go-to-tab-name "PSO_RS"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pso_random_search 16 &
else
  echo "No ZELLIJ session"
fi
