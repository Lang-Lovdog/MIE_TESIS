# Choix du terminal (décommentez celui qui fonctionne chez vous)
 set terminal qt size 1300,510
# set terminal wxt size 1300,510
# set terminal x11 size 1300,510

# Séparateur et style
set datafile separator comma
set style line 1 lc rgb 'blue' lw 2
set style line 2 lc rgb 'red'  lw 2
set zeroaxis
set grid

# Définir des coefficients et des modules
AH3  =  0.24018
AF3  =  0.77046
AF5  =  0.97955
A3N3 = -1.6974
AD5  =  0.43564
s0   =  1.7911
tau0 =  1.5603
s1   =  2.4473
tau1 =  3.8434


# Définir les fonctions
Veff     (s, tau) = AH3*s/tau**3 + AF3/(s*tau**3) + AF5/tau**4 + A3N3/tau**3
Veff_lift(s, tau) = Veff(s, tau) + AD5/(sqrt(s)*tau**(2.5))

# Plages
s_min   = 0.5 * s0
s_max   = 2.5 * s0
tau_min = 0.5 * tau0
tau_max = 5.5 * tau0

# Plage pour l'encart (zoom sur τ)
tau_zoom_min = 0.9 * tau0
tau_zoom_max = 2.1 * tau0   # ou 1.1 * tau0 selon le notebook

# Graphiques
set multiplot layout 1,3

set xlabel 's'
set ylabel 'V(s, τ₀)'
set title sprintf('V(s) avec τ = %.4f', tau0)
plot [s=s_min:s_max] Veff_lift(s, tau0) ls 1 title 'avec AD5', \
                     Veff     (s, tau0) ls 2 title 'sans AD5'

set xlabel 'τ'
set ylabel 'V(s₀, τ)'
set title sprintf('V(τ) avec s = %.4f', s0)
plot [tau=tau_min:tau_max] Veff_lift(s0, tau) ls 1 title 'avec AD5', \
                           Veff     (s1, tau) ls 2 title 'sans AD5'

#set size 0.3,0.3
#set origin 0.65,0.6
set xlabel 'τ (zoom)'
set ylabel 'V'
set title 'Zoom autour du minimum'
set xrange [tau_zoom_min:tau_zoom_max]
#set yrange [0:0.00021]
set grid
# On ne trace que la courbe avec lifting (celle de l'encart original)
plot [tau=tau_zoom_min:tau_zoom_max] Veff_lift(s1, tau) ls 1 notitle

unset multiplot

