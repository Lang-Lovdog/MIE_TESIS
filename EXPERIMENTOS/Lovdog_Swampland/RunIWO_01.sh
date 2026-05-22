#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "IWO_GRID" -c "$(pwd)" -l default -- toilet "IWO GRID"
  zellij ac go-to-tab-name "IWO_GRID"
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid 0 4  8 12 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid 1 5  9 13 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid 2 6 10 14 &
  sleep 2
  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_iwo_grid 3 7 11 15 &
else
  echo "No ZELLIJ session"
fi

