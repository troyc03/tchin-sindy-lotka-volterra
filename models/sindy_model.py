import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pysindy as ps
from lotka_volterra import lotka_volterra
from pysindy import SINDy
from pysindy.optimizers import STLSQ

# Define the parameters for the Lotka-Volterra model
alpha, beta = 1.5, 1.0
delta, gamma = 0.5, 1.0

# Define the initial conditions and time span for the simulation
initial_conditions = [10.0, 5.0]  # Initial populations of prey and predator
t_span = (0, 20)  # Time span for the simulation
t_eval = np.linspace(t_span[0], t_span[1], 400)

# Simulate the Lotka-Volterra system
solution = solve_ivp(
    lotka_volterra,
    t_span,
    initial_conditions,
    args=(alpha, beta, delta, gamma),
    t_eval=t_eval,
    method='RK45'
)

# Extract the time and state variables from the solution
t = solution.t
x = solution.y[0]  # Prey population
y = solution.y[1]  # Predator population    

# Build the state matrix for SINDy
X = np.vstack((x, y)).T  # Shape: (n_samples, n_features)   
y = np.vstack((np.gradient(x, t), np.gradient(y, t))).T  # Shape: (n_samples, n_features)   

# Define the SINDy model with finite difference differentiation and STLSQ optimizer
optimizer = STLSQ(threshold=0.1)
model = SINDy(optimizer=optimizer, feature_library=ps.PolynomialLibrary(degree=2), differentiation_method=ps.FiniteDifference())  

# Fit the SINDy model to the data
model.fit(X, t=t, x_dot=y)

# Print the discovered equations
model.print()

# Simulate the discovered model
t_sim = np.linspace(0, 20, 400)
X_sim = model.simulate(X[0], t_sim)

# Plot the original and simulated data for comparison
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(t, x, label='Original Prey (x)', color='tab:blue', linewidth=2)
plt.plot(t_sim, X_sim[:, 0], '--', label='Simulated Prey (x)', color='tab:blue', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Prey Population Comparison')
plt.grid(True, linestyle='--', alpha=0.6)
plt.subplot(1, 2, 2)
plt.plot(t, y, label='Original Predator (y)', color='tab:orange', linewidth=2)
plt.plot(t_sim, X_sim[:, 1], '--', label='Simulated Predator (y)', color='tab:orange', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Predator Population Comparison')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.legend()    
plt.show()