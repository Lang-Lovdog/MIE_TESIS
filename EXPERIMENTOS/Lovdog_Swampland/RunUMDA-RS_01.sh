#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "UMDA_GRID" -c "$(pwd)" -l default -- toilet "UMDA RANDOM SEARCH"
  zellij ac go-to-tab-name "UMDA_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_umda_random_search  16 &
else
  echo "No ZELLIJ session"
fi


