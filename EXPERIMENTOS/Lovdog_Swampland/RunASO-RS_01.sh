#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "ASO_GRID" -c "$(pwd)" -l default -- toilet "ASO RANDOM SEARCH"
  zellij ac go-to-tab-name "ASO_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_aso_random_search  16 &
else
  echo "No ZELLIJ session"
fi

