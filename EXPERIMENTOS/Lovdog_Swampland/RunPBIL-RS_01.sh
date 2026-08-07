#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "PBIL_GRID" -c "$(pwd)" -l default -- toilet "PBIL RANDOM SEARCH"
  zellij ac go-to-tab-name "PBIL_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_pbil_random_search  16 &
else
  echo "No ZELLIJ session"
fi


