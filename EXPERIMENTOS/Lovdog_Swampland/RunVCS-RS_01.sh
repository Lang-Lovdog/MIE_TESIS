#!/bin/bash

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "VCS_GRID" -c "$(pwd)" -l default -- toilet "VCS RANDOM SEARCH"
  zellij ac go-to-tab-name "VCS_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_vcs_random_search  16 &
else
  echo "No ZELLIJ session"
fi

