	a=0; while [ $a -lt 40 ]; do ./exe | tail -n 2 | head -n 1 >> resultados.txt; sleep 0.5; a=$(( $a + 1 )); done
