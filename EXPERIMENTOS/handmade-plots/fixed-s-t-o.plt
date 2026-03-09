# Choix du terminal (décommentez celui qui fonctionne chez vous)
 set terminal qt size 1300,510
# set terminal wxt size 1300,510
# set terminal x11 size 1300,510


idx=0
while(idx<8) {
# Nom du fichier CSV
filename = sprintf("../Lovdog_Swampland/VacuaFound_17022026/found_solutions_AdS_fv_%d.csv", idx)


# Séparateur et styles
set datafile separator comma
set style line 1 lc rgb 'blue'   lw 1          # nouveau avec AD5
set style line 2 lc rgb 'red'    lw 1          # nouveau sans AD5
set style line 3 lc rgb 'cyan'   lw 1 dt 2     # original avec AD5 (pointillés)
set style line 4 lc rgb 'magenta'lw 1 dt 2     # original sans AD5 (pointillés)

set samples 400

set zeroaxis

# Lecture des coefficients de la première ligne de données (ligne 2)
# Nouveaux coefficients (sans _O)
stats filename using 4  every ::1::1 nooutput; AH3   = STATS_min
stats filename using 6  every ::1::1 nooutput; AF3   = STATS_min
stats filename using 8  every ::1::1 nooutput; AF5   = STATS_min
stats filename using 10 every ::1::1 nooutput; A3N3  = STATS_min
stats filename using 12 every ::1::1 nooutput; AD5   = STATS_min
# Coefficients originaux (avec _O)
stats filename using 5  every ::1::1 nooutput; AH3_O = STATS_min
stats filename using 7  every ::1::1 nooutput; AF3_O = STATS_min
stats filename using 9  every ::1::1 nooutput; AF5_O = STATS_min
stats filename using 11 every ::1::1 nooutput; A3N3_O= STATS_min
stats filename using 13 every ::1::1 nooutput; AD5_O = STATS_min
# Champs s et tau (communs)
stats filename using 14 every ::1::1 nooutput; s0    = STATS_min
stats filename using 15 every ::1::1 nooutput; tau0  = STATS_min

# Définition des fonctions de potentiel
# Nouveaux
Veff(s, tau)     = AH3*s/tau**3 + AF3/(s*tau**3) + AF5/tau**4 + A3N3/tau**3
Veff_lift(s, tau)= Veff(s, tau) + AD5/(sqrt(s)*tau**(2.5))
# Originaux
Veff_orig(s, tau)     = AH3_O*s/tau**3 + AF3_O/(s*tau**3) + AF5_O/tau**4 + A3N3_O/tau**3
Veff_lift_orig(s, tau)= Veff_orig(s, tau) + AD5_O/(sqrt(s)*tau**(2.5))

# Plages (basées sur les valeurs communes)
s_min   = 0.2 * s0
s_max   = 1.5 * s0
tau_min = 0.2 * tau0
tau_max = 2.5 * tau0

# Graphiques
set multiplot layout 1,2

# Graphique en fonction de s
set xlabel 's'
set ylabel 'V(s, τ₀)'
set title sprintf('V(s) avec τ = %.4f', tau0)
plot [s=s_min:s_max] Veff_lift(s, tau0) ls 1 title 'nouveau avec AD5', \
                     Veff(s, tau0) ls 2 title 'nouveau sans AD5', \
                     Veff_lift_orig(s, tau0) ls 3 title 'original avec AD5', \
                     Veff_orig(s, tau0) ls 4 title 'original sans AD5'

# Graphique en fonction de τ
set xlabel 'τ'
set ylabel 'V(s₀, τ)'
set title sprintf('V(τ) avec s = %.4f', s0)
plot [tau=tau_min:tau_max] Veff_lift(s0, tau) ls 1 title 'nouveau avec AD5', \
                           Veff(s0, tau) ls 2 title 'nouveau sans AD5', \
                           Veff_lift_orig(s0, tau) ls 3 title 'original avec AD5', \
                           Veff_orig(s0, tau) ls 4 title 'original sans AD5'

unset multiplot

pause(5)
idx = idx + 1
}
