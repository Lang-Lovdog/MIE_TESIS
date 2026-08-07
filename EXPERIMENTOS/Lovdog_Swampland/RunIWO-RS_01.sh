#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "IWO_GRID" -c "$(pwd)" -l default -- toilet "IWO RANDOM SEARCH"
  zellij ac go-to-tab-name "IWO_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_random_search  16 &
else
  echo "No ZELLIJ session"
fi

