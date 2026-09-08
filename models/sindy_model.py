import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pysindy as ps

alpha, beta = 1.1, 0.4
delta, gamma = 0.1, 0.4

def lotka_volterra(t, z):
    x, y = z
    return [alpha * x - beta * x * y, delta * x * y - gamma * y]

t_span = (0,40)
t_eval = np.linspace(t_span[0], t_span[1], 1000)
z0 = [10.0, 5.0]

sol = solve_ivp(lotka_volterra, t_span, z0, t_eval=t_eval)
X = sol.y.T

np.random.seed(42)
noise_level = 0.05
X_noisy = X + noise_level * np.std(X, axis=0) * np.random.randn(*X.shape)

feature_names = ["x", "y"]
poly_library = ps.PolynomialLibrary(degree=2)
optimizer = ps.STLSQ(threshold=0.1)

model = ps.SINDy(
    feature_library=poly_library,
    optimizer=optimizer,
)
model.fit(X_noisy, t=t_eval)

X_sim = model.simulate(z0, t_eval)

fig, axs = plt.subplots(1, 2, figsize=(14, 5))

axs[0].plot(t_eval, X[:, 0], 'k-', label='True Prey', alpha=0.7)
axs[0].plot(t_eval, X[:, 1], 'b-', label='True Predator', alpha=0.7)
axs[0].plot(t_eval, X_sim[:, 0], 'r--', label='SINDy Prey')
axs[0].plot(t_eval, X_sim[:, 1], 'g--', label='SINDy Predator')
axs[0].scatter(t_eval[::20], X_noisy[::20, 0], color='black', alpha=0.3, label='Noisy Prey Data', s=10)
axs[0].scatter(t_eval[::20], X_noisy[::20, 1], color='blue', alpha=0.3, label='Noisy Predator Data', s=10)
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Population')
axs[0].set_title('Solution Plot (Time Series)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(X[:, 0], X[:, 1], 'k-', label='True Trajectory', alpha=0.7)
axs[1].plot(X_sim[:, 0], X_sim[:, 1], 'r--', label='SINDy Trajectory')
axs[1].scatter(X_noisy[::20, 0], X_noisy[::20, 1], color='purple', alpha=0.3, label='Noisy Data Points', s=10)
axs[1].set_xlabel('Prey Population (x)')
axs[1].set_ylabel('Predator Population (y)')
axs[1].set_title('Phase Portrait')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()

print("--- Discovered Equations ---")
model.print()
