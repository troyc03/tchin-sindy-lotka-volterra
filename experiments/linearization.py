import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

alpha, beta, gamma, delta = 1.0, 1.0, 1.0, 1.0

x_bar = gamma / delta
y_bar = alpha / beta

A = np.array([
    [0.0, -beta * x_bar],
    [delta * y_bar, 0.0]
])

def nonlinear_system(state, t):
    x, y = state
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

def linear_system(du_state, t):
    du = np.array(du_state)
    dudt = A @ du
    return dudt.tolist()

t = np.linspace(0, 50, 1000)

# Small perturbation away from the equilibrium point
du0 = [0.2, -0.1] 
initial_nonlinear = [x_bar + du0[0], y_bar + du0[1]]

# Solve both systems
sol_nonlinear = odeint(nonlinear_system, initial_nonlinear, t)
sol_linear_du = odeint(linear_system, du0, t)

# Convert linear perturbation back to absolute population coordinates for comparison
sol_linear_abs_x = x_bar + sol_linear_du[:, 0]
sol_linear_abs_y = y_bar + sol_linear_du[:, 1]

# Plotting the comparison
plt.figure(figsize=(10, 5))
plt.plot(t, sol_nonlinear[:, 0], 'b-', label='Non-linear Prey (x)')
plt.plot(t, sol_linear_abs_x, 'b--', label='Linearized Prey (x)')
plt.plot(t, sol_nonlinear[:, 1], 'r-', label='Non-linear Predator (y)')
plt.plot(t, sol_linear_abs_y, 'r--', label='Linearized Predator (y)')
plt.title('Comparison of Non-linear vs. Linearized Lotka-Volterra')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.grid(True)
plt.show()

