#!/bin/bash

model=$1
shift
## Si el segundo argumento es -d=texto, se guarda en pdir
if [[ $1 == -d=* ]]; then
  pdir="$1"
  shift
else
  pdir=""
fi
midx="$@"

if [ ! -z $ZELLIJ ]; then
  zellij ac new-tab -n "$model $midx" -c "$(pwd)" -l default -- toilet "$model $midx RANDOM SEARCH"
  zellij ac go-to-tab-name "$model_RS"

  zellij ac new-pane -- ./BASH_SCRIPTS/run_da_libre_random_search "$model" "$pdir" "$midx" &
else
  echo "No ZELLIJ session"
fi

