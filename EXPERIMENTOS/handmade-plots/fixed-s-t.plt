# Définir le chemin du fichier CSV (ajustez selon votre arborescence)
filename = "../Lovdog_Swampland/VacuaFound_17022026/found_solutions_AdS_fv_0.csv"

# Vérification simple : si le fichier n'existe pas, on tente un chemin absolu
# Note : Gnuplot n'a pas de fonction native file_exists, on se contente d'essayer
# et en cas d'erreur, le script s'arrêtera.

# Séparateur et style
set datafile separator comma
set style line 1 lc rgb 'blue' lw 2
set style line 2 lc rgb 'red'  lw 2

# Lire la première ligne de données (ligne 2) et stocker les valeurs
stats filename using 4 every ::1::1 nooutput
AH3 = STATS_min
stats filename using 6 every ::1::1 nooutput
AF3 = STATS_min
stats filename using 8 every ::1::1 nooutput
AF5 = STATS_min
stats filename using 10 every ::1::1 nooutput
A3N3 = STATS_min
stats filename using 12 every ::1::1 nooutput
AD5 = STATS_min
stats filename using 14 every ::1::1 nooutput
s0 = STATS_min
stats filename using 15 every ::1::1 nooutput
tau0 = STATS_min

# Définir les fonctions
Veff     (s, tau) = AH3*s/tau**3 + AF3/(s*tau**3) + AF5/tau**4 + A3N3/tau**3
Veff_lift(s, tau) = Veff(s, tau) + AD5/(sqrt(s)*tau**(2.5))

# Plages
s_min   = 0.5 * s0
s_max   = 2.5 * s0
tau_min = 0.5 * tau0
tau_max = 5.5 * tau0

# Graphiques
set multiplot layout 1,2

set xlabel 's'
set ylabel 'V(s, τ₀)'
set title sprintf('V(s) avec τ = %.4f', tau0)
plot [s=s_min:s_max] Veff_lift(s, tau0) ls 1 title 'avec AD5', \
                     Veff(s, tau0) ls 2 title 'sans AD5'

set xlabel 'τ'
set ylabel 'V(s₀, τ)'
set title sprintf('V(τ) avec s = %.4f', s0)
plot [tau=tau_min:tau_max] Veff_lift(s0, tau) ls 1 title 'avec AD5', \
                       Veff(s0, tau) ls 2 title 'sans AD5'

unset multiplot
