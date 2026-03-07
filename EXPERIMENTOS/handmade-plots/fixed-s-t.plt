# Paramètres extraits du CSV (à remplacer par vos valeurs)
AH3 = 0.166049
AF3 = 0.114358
AF5 = 0.033838
AO3 = -0.405598
AD5 = 0.249097   # si présent
s0 = 1.343635
tau0 = 4.245118

# Définition des fonctions
V_full(s,tau) = AH3*s/tau**3 + AF3/(s*tau**3) + AF5/tau**4 + AO3/tau**3 + AD5/(sqrt(s)*tau**(2.5))
V_noad5(s,tau) = AH3*s/tau**3 + AF3/(s*tau**3) + AF5/tau**4 + AO3/tau**3

# Plages
s_min = 0.5 * s0
s_max = 2.5 * s0
tau_min = 0.5 * tau0
tau_max = 5.5 * tau0

# Style
set style line 1 lc rgb 'blue' lw 2
set style line 2 lc rgb 'red' lw 2

# Graphique 1 : V(s) à tau fixé
set multiplot layout 1,2

set xlabel 's'
set ylabel 'V(s, τ₀)'
set title sprintf('V(s) avec τ = %.4f', tau0)
plot [s_min:s_max] V_full(s, tau0) ls 1 title 'avec AD5', \
                   V_noad5(s, tau0) ls 2 title 'sans AD5'

# Graphique 2 : V(τ) à s fixé
set xlabel 'τ'
set ylabel 'V(s₀, τ)'
set title sprintf('V(τ) avec s = %.4f', s0)
plot [tau_min:tau_max] V_full(s0, tau) ls 1 title 'avec AD5', \
                       V_noad5(s0, tau) ls 2 title 'sans AD5'

unset multiplot
