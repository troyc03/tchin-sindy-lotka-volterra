import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pysindy as ps

# Definining the Lotka-Volterra system directly to make the script self-contained
def lotka_volterra(state, t, alpha, beta, delta, gamma):
    x, y = state
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

# Define the parameters for the Lotka-Volterra model
alpha, beta = 1.1, 0.4
delta, gamma = 0.1, 0.4

# Define the initial conditions and time span for the simulation
initial_conditions = [2.0, 1.0] # Lowered initial conditions to prevent extreme exponentials
t_span = (0, 20) 
t_eval = np.linspace(t_span[0], t_span[1], 400)

# Simulate the Lotka-Volterra system
solution = odeint(lotka_volterra, initial_conditions, t_eval, args=(alpha, beta, delta, gamma))

# Extract the time and state variables from the solution
t = t_eval
x = solution[:, 0] # Prey population
y = solution[:, 1] # Predator population

# Build the state matrix for SINDy
X = np.vstack((x, y)).T 

# Define the SINDy model
model = ps.SINDy(
    optimizer=ps.STLSQ(threshold=0.05),
    feature_library=ps.PolynomialLibrary(degree=2), 
    differentiation_method=ps.FiniteDifference()
)

# Fit the SINDy model directly to unscaled data
model.fit(X, t=t)

# Print the discovered equations
print("Discovered Equations:")
model.print()

# Simulate the discovered model using the original initial conditions
X_sim = model.simulate(X[0], t)

# Plot the original and simulated data for comparison
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(t, x, label='Original Prey (x)', color='tab:blue', linewidth=2)
plt.plot(t, X_sim[:, 0], '--', label='Simulated Prey (x)', color='tab:cyan', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Prey Population Comparison')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.subplot(1, 2, 2)
plt.plot(t, y, label='Original Predator (y)', color='tab:orange', linewidth=2)
plt.plot(t, X_sim[:, 1], '--', label='Simulated Predator (y)', color='tab:red', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Predator Population Comparison')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
