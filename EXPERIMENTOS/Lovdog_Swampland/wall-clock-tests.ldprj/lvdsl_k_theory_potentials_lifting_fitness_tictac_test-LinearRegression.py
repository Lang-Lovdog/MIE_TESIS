import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the CSV file into a DataFrame
data = pd.read_csv('lvdsl_k_theory_potentials_lifting_fitness_tictac_test.csv')

# Set the theme for Seaborn with "plasma" palette
sns.set_theme(style="whitegrid", palette="plasma")  # Plasma theme

# Plot N vs t (Total Time) and fit a linear regression line
plt.figure(figsize=(10, 6))

# Perform linear regression
X = data['N'].values.reshape(-1, 1)
y = data['t']
model = LinearRegression()
model.fit(X, y)

# Get the coefficients of the linear model
slope, intercept = model.coef_[0], model.intercept_

# Plot the original data points
sns.scatterplot(x='N', y='t', data=data, label='Original Data')

# Plot the fitted line
plt.plot(data['N'], model.predict(X), color='red', label=f'Fitted Line (y = {slope:.2f}x + {intercept:.2f})')

plt.title(r'$N$ vs. $t$')
plt.xlabel(r'$N$')
plt.ylabel(r'$t$ (seconds)')
plt.legend()
plt.show()

# Print the slope and intercept of the fitted line
print(f"Slope: {slope:.2f}, Intercept: {intercept:.2f}")

