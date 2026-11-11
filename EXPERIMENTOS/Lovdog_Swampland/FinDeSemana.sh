#!/bin/bash

echo "Fin de semana ocupado uwu"
echo ""

./RunLibre-RS.sh PSO -d=lvdsl_outputs/VacuaFound_20261030 321
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 5766
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 12043

echo "Esperando 12 horas para iniciar"
sleep 12h

# Par 1
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 12043
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 9556
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 2
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261027 5891
./RunLibre-RS.sh PSO -d=lvdsl_outputs/VacuaFound_20261101 926
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 3
./RunLibre-RS.sh ACO -d=lvdsl_outputs/VacuaFound_20261103 24071
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 2876
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 4
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261027 65131
./RunLibre-RS.sh ACO -d=lvdsl_outputs/VacuaFound_20261106 3305
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 5
./RunLibre-RS.sh GA -d=lvdsl_outputs/VacuaFound_20260728 74
./RunLibre-RS.sh IWO -d=lvdsl_outputs/VacuaFound_20260728 1538
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 6
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261027 50699
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261030 42041
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 7
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 572
./RunLibre-RS.sh GA -d=lvdsl_outputs/VacuaFound_20260728 492
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 8
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261030 51520
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261027 39031
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 9
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261006 67570
./RunLibre-RS.sh PSO -d=lvdsl_outputs/VacuaFound_20261028 758
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 10
./RunLibre-RS.sh ACO -d=lvdsl_outputs/VacuaFound_20261103 157
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 2897
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 11
./RunLibre-RS.sh PSO -d=lvdsl_outputs/VacuaFound_20261028 883
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20260930 71334
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 12
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261103 3560
./RunLibre-RS.sh PBIL -d=lvdsl_outputs/VacuaFound_20260728 7792
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 13
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261030 20675
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20260930 53093
echo "Esperando 12 horas antes del siguiente lote"
sleep 12h

# Par 14
./RunLibre-RS.sh ASO -d=lvdsl_outputs/VacuaFound_20261005 62057
./RunLibre-RS.sh ACO -d=lvdsl_outputs/VacuaFound_20261027 7796
echo "Todos los lotes han finalizado."

