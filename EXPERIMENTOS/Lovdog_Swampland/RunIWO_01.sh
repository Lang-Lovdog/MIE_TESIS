#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "IWO_GRID" -c "$(pwd)" -l default -- toilet "IWO GRID"
  zellij ac go-to-tab-name "IWO_GRID"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  4 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  5 &
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  6 &

  #zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  8 12 &
  #zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  9 13 &
  #zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid 10 14 &
  #zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid  7 11 15 &
else
  echo "No ZELLIJ session"
fi

