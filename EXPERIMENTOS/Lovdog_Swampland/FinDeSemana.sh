#!/bin/bash

echo "Fin de semana ocupado uwu"
echo ""
./RunLibre-RS.sh  VCS -d=lvdsl_outputs/VacuaFound_20261103 12043
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh VCS -d=lvdsl_outputs/VacuaFound_20261103 9556
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh  ASO -d=lvdsl_outputs/VacuaFound_20261027 5891
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h 
./RunLibre-RS.sh  PSO -d=lvdsl_outputs/VacuaFound_20261101 926
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h 
./RunLibre-RS.sh  ACO -d=lvdsl_outputs/VacuaFound_20261103 24071
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh  VCS -d=lvdsl_outputs/VacuaFound_20261103 2876
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261027 65131
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh ACO  -d=lvdsl_outputs/VacuaFound_20261106 3305
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh GA   -d=lvdsl_outputs/VacuaFound_20260728 74
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh IWO  -d=lvdsl_outputs/VacuaFound_20260728 1538
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261027 50699
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261030 42041
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh VCS  -d=lvdsl_outputs/VacuaFound_20261103 572
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh GA   -d=lvdsl_outputs/VacuaFound_20260728 492
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261030 51520
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261027 39031
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261006 67570
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh PSO  -d=lvdsl_outputs/VacuaFound_20261028 758
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ACO  -d=lvdsl_outputs/VacuaFound_20261103 157
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh VCS  -d=lvdsl_outputs/VacuaFound_20261103 2897
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh PSO  -d=lvdsl_outputs/VacuaFound_20261028 883
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20260930 71334
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261103 3560
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh PBIL -d=lvdsl_outputs/VacuaFound_20260728 7792
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261030 20675
echo "Esperando 4 horas antes del siguiente lote"
sleep 4h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20260930 53093
echo "Esperando 7 horas antes del siguiente lote"
sleep 7h
./RunLibre-RS.sh ASO  -d=lvdsl_outputs/VacuaFound_20261005 62057
echo "Esperando 5 horas antes del siguiente lote"
sleep 5h
./RunLibre-RS.sh ACO  -d=lvdsl_outputs/VacuaFound_20261027 7796

