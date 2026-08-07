import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv('lvdsl_k_theory_potentials_lifting_fitness_tictac_test.csv')

# Set the theme for Seaborn with "plasma" palette
sns.set_theme(style="whitegrid", palette="plasma")  # Plasma theme

# Plot N vs t (Total Time)
plt.figure(figsize=(10, 6))
sns.lineplot(x='N', y='t', data=data)
plt.title(r'$N$ vs. $t$')
plt.xlabel(r'$N$')
plt.ylabel(r'$t$ (seconds)')
plt.show()

# Set the theme for Seaborn with "viridis" palette
sns.set_theme(style="whitegrid", palette="viridis")  # Viridis theme

# Plot N vs bar_t (Avg per Eval)
plt.figure(figsize=(10, 6))
sns.lineplot(x='N', y='bar_t', data=data)
plt.title(r'$N$ vs. $\bar{t}$')
plt.xlabel(r'$N$')
plt.ylabel(r'$\bar{t}$ (seconds)')
plt.show()
