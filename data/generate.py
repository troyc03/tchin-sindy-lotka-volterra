import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import os

def lotka_volterra(t, z, alpha, beta, delta, gamma):
    """
    Defines the differential equations for the Lotka-Volterra model.
    """
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

def generate_synthetic_data():
    # Ground truth parameters
    alpha = 1.5
    beta = 1.0
    delta = 0.5
    gamma = 1.0
    
    # Initial conditions: Prey = 10, Predator = 5
    z0 = [10.0, 5.0]
    
    # Time span for the simulation
    t_start = 0
    t_end = 20
    num_points = 400
    t_eval = np.linspace(t_start, t_end, num_points)
    
    # Integrate the ODEs
    print("Simulating Lotka-Volterra system...")
    solution = solve_ivp(
        lotka_volterra, 
        [t_start, t_end], 
        z0, 
        args=(alpha, beta, delta, gamma), 
        t_eval=t_eval,
        method='RK45'
    )
    
    # Extract states
    t = solution.t
    x = solution.y[0]
    y = solution.y[1]
    
    # Add optional Gaussian noise to simulate realistic experimental data (e.g., 2% noise)
    np.random.seed(42)  # For reproducibility
    noise_level = 0.02
    x_noisy = x + np.random.normal(0, noise_level * np.mean(x), size=x.shape)
    y_noisy = y + np.random.normal(0, noise_level * np.mean(y), size=y.shape)
    
    # Combine into a pandas DataFrame
    data = pd.DataFrame({
        'time': t,
        'prey_clean': x,
        'predator_clean': y,
        'prey_noisy': x_noisy,
        'predator_noisy': y_noisy
    })
    
    # Save datasets
    os.makedirs('data/raw', exist_ok=True)
    data.to_csv('data/raw/lotka_volterra_data.csv', index=False)
    print("Data generation complete. Saved to 'data/raw/lotka_volterra_data.csv'.")

if __name__ == '__main__':
    generate_synthetic_data()
