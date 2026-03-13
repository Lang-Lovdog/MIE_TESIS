#a=0; while [ $a -lt 40 ]; do ./ags_exe | tail -n 2 | head -n 1; done #>> resultados_ags.txt; sleep 0.5; a=$(( $a + 1 )); done
a=0; while [ $a -lt 90 ]; do
    res="$(./ags_exe)"
		printf "%s\n" "$res"
		printf "%s\n" "$res" >> resultados_ags.txt
		sleep 0.5;
		a=$(( $a + 1 ));
done
