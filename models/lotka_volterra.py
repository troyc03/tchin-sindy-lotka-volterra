import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def lotka_volterra(t, z, alpha, beta, delta, gamma):
    x, y = z
    x_dot = alpha * x - beta * x * y
    y_dot = delta * x * y - gamma * y

    return [x_dot, y_dot]

alpha, beta = 1.1, 0.4
delta, gamma = 0.1, 0.4

initial_pop = [10.0, 5.0]
t_span = (0,70)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

sol = solve_ivp(
    lotka_volterra,
    t_span,
    initial_pop,
    args=(alpha, beta, delta, gamma),
    t_eval=t_eval
)

time = sol.t
prey = sol.y[0]
pred = sol.y[1]

# 4. Plot the results
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(time, prey, label='Prey (e.g., Rabbits)', color='tab:blue', linewidth=2)
plt.plot(time, pred, label='Predator (e.g., Foxes)', color='tab:orange', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Predator-Prey Dynamics Over Time')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(prey, pred, color='tab:purple', linewidth=2)
plt.xlabel('Prey Population')
plt.ylabel('Predator Population')
plt.title('Phase Space Orbit')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

