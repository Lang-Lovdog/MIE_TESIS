#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "ACO_GRID" -c "$(pwd)" -l default -- toilet "ACO RANDOM SEARCH"
  zellij ac go-to-tab-name "ACO_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_aco_random_search  16 &
else
  echo "No ZELLIJ session"
fi

