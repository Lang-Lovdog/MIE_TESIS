import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Load the CSV file into a DataFrame
#data = pd.read_csv('lvdsl_k_theory_potentials_lifting_fitness_tictac_test.csv')
#data = pd.read_csv('lvdsl_k_theory_potentials_lifting_fitness_tictac_test-1.csv')
data = pd.read_csv('lvdsl_k_theory_potentials_lifting_fitness_tictac_test-2.csv')

# Set the theme for Seaborn with "plasma" palette (for N vs t)
sns.set_theme(style="whitegrid", palette="plasma")  # Plasma theme for N vs t

# Plot N vs t and fit linear regression line
plt.figure(figsize=(10, 6))

# Perform linear regression
X = data['N'].values.reshape(-1, 1)
y = data['t']
model = LinearRegression()
model.fit(X, y)

# Get the coefficients of the linear model
slope, intercept = model.coef_[0], model.intercept_

# Plot the original data points and fitted line (linear regression)
sns.scatterplot(x='N', y='t', data=data, label='Original Data')
plt.semilogx(data['N'], model.predict(X), color='red', label=f'Linear Fit (y = {slope:.2f}x + {intercept:.2f})')

# Perform 2nd and 3rd order polynomial regression
poly2 = PolynomialFeatures(degree=2)
X_poly2 = poly2.fit_transform(X)
model2 = LinearRegression()
model2.fit(X_poly2, y)

poly3 = PolynomialFeatures(degree=3)
X_poly3 = poly3.fit_transform(X)
model3 = LinearRegression()
model3.fit(X_poly3, y)

# Plot the 2nd and 3rd order polynomial fits
plt.semilogx(data['N'], model2.predict(poly2.transform(X)), color='blue', label=f'Quadratic Fit (y = {model2.coef_[1]:.2f}x^2 + ...)')
plt.semilogx(data['N'], model3.predict(poly3.transform(X)), color='green', label=f'Cubic Fit (y = {model3.coef_[2]:.2f}x^3 + ...)')

# Add labels and legend
plt.title(r'$N$ vs. $t$')
plt.xlabel(r'$N$ (log)')
plt.ylabel(r'$t$')
plt.legend()

#plt.savefig('./N_t.analysis.png')
#plt.savefig('./N_t.analysis-1.png')
plt.savefig('./N_t.analysis-2.png')
plt.show()

# Set the theme for Seaborn with "viridis" palette (for N vs t_inv)
sns.set_theme(style="whitegrid", palette="viridis")  # Viridis theme for N vs t_inv

# Plot N vs t_inv
plt.figure(figsize=(10, 6))

# Perform linear regression on t_inv
t_inv = 1 / data['t']
model_inv = LinearRegression()
model_inv.fit(X, t_inv)

# Get the coefficients of the inverse linear model
slope_inv, intercept_inv = model_inv.coef_[0], model_inv.intercept_

# Plot the original data points and fitted line (linear regression)
sns.scatterplot(x='N', y='t_inv', data=data.assign(t_inv=1 / data['t']), label='Original Data')
plt.semilogx(data['N'], model_inv.predict(X), color='red', label=f'Linear Fit (y = {slope_inv:.2f}x + {intercept_inv:.2f})')

# Perform 2nd and 3rd order polynomial regression
poly2_inv = PolynomialFeatures(degree=2)
X_poly2_inv = poly2.transform(X)
model2_inv = LinearRegression()
model2_inv.fit(X_poly2_inv, t_inv)

poly3_inv = PolynomialFeatures(degree=3)
X_poly3_inv = poly3.transform(X)
model3_inv = LinearRegression()
model3_inv.fit(X_poly3_inv, t_inv)

# Plot the 2nd and 3rd order polynomial fits
plt.semilogx(data['N'], model2_inv.predict(poly2.transform(X)), color='blue', label=f'Quadratic Fit (y = {model2_inv.coef_[1]:.2f}x^2 + ...)')
plt.semilogx(data['N'], model3_inv.predict(poly3.transform(X)), color='green', label=f'Cubic Fit (y = {model3_inv.coef_[2]:.2f}x^3 + ...)')

# Add labels and legend
plt.title(r'$N$ vs. $t^{-1}$')
plt.xlabel(r'$N$ (log)')
plt.ylabel(r'$t^{-1}$')
plt.legend()

#plt.savefig('./N_t_inv.analysis.png')
#plt.savefig('./N_t_inv.analysis-1.png')
plt.savefig('./N_t_inv.analysis-2.png')
plt.show()

# Print the slope and intercept of the fitted inverse linear model
print(f"Inverse Linear Fit: Slope = {slope_inv:.2f}, Intercept = {intercept_inv:.2f}")
