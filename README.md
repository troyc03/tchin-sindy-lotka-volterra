# SINDy Lotka–Volterra

**Discovering nonlinear predator–prey dynamics from data using Sparse Identification of Nonlinear Dynamics (SINDy).**

This project explores how data-driven system identification can recover the governing equations of a nonlinear dynamical system. Using the classical Lotka–Volterra predator–prey model, it simulates population dynamics, generates synthetic observations, and applies SINDy to identify the underlying relationships between prey and predator populations.

## Overview

The [Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) describe the interaction between two populations: a prey population that grows in the absence of predators and a predator population whose growth depends on prey availability.

The governing equations are


$\frac{dx}{dt} = \alpha x - \beta xy$

$\frac{dy}{dt} = \delta xy - \gamma y$

where:

- \(x\) is the prey population.
- \(y\) is the predator population.
- \(\alpha\) is the prey growth rate.
- \(\beta\) describes the effect of predation on the prey population.
- \(\gamma\) is the predator death rate.
- \(\delta\) describes the contribution of prey to predator growth.

The model produces coupled, nonlinear population dynamics. Rather than relying only on the known equations, this project uses **Sparse Identification of Nonlinear Dynamics (SINDy)** to infer a mathematical model from simulated time-series data.

## Objectives

- Simulate the Lotka–Volterra predator–prey system.
- Generate synthetic population data with and without measurement noise.
- Apply SINDy to identify the system's governing equations.
- Compare trajectories predicted by the discovered model against the original simulation.
- Visualize population dynamics and phase-space behavior.
- Explore the relationship between nonlinear dynamics and local linear approximations.

## Methodology

### 1. Simulate the dynamical system

The Lotka–Volterra equations are numerically integrated to generate time-series data for the prey and predator populations.

The simulations provide a reference system with known governing equations and parameters.

### 2. Generate synthetic data

The data-generation script produces observations over a specified time interval. It records both the clean simulated populations and noisy observations.

The generated dataset contains the following columns:

| Column | Description |
|---|---|
| `time` | Simulation time |
| `prey_clean` | Prey population without added noise |
| `predator_clean` | Predator population without added noise |
| `prey_noisy` | Prey population with added Gaussian noise |
| `predator_noisy` | Predator population with added Gaussian noise |

The current generator uses a fixed random seed for reproducibility and adds Gaussian noise at 2% of each population's mean.

### 3. Identify the governing equations with SINDy

SINDy identifies a parsimonious model by selecting relevant candidate functions from a library of possible terms.

For this project, the implementation uses:

- **Polynomial feature library:** Includes candidate terms up to degree two.
- **Finite-difference differentiation:** Estimates time derivatives from sampled data.
- **Sequentially Thresholded Least Squares (STLSQ):** Promotes sparse models by removing coefficients below a specified threshold.

The discovered equations can then be compared with the original Lotka–Volterra equations to assess whether the identification procedure recovers the expected linear and interaction terms.

### 4. Evaluate and visualize the model

The SINDy implementation prints the discovered equations and simulates the identified system. Its plots compare the original and reconstructed prey and predator trajectories.

Additional scripts visualize the nonlinear population dynamics and compare the nonlinear system with a local linearization near its equilibrium.

## Repository Structure

```text
tchin-sindy-lotka-volterra/
├── data/
│   ├── generate.py
│   ├── raw/
│   │   └── lotka_volterra_data.csv
│   └── processed/
│       └── lotka_volterra_data_cleaned.csv
├── experiments/
│   ├── error_analysis.py
│   └── linearization.py
├── models/
│   ├── lotka_volterra.py
│   └── sindy_model.py
├── notebooks/
│   └── data_analysis.ipynb
├── LICENSE
└── README.md
```

### Key files

| File | Purpose |
|---|---|
| `data/generate.py` | Simulates the Lotka–Volterra system and generates clean and noisy synthetic data. |
| `data/raw/lotka_volterra_data.csv` | Stores the generated raw dataset. |
| `data/processed/lotka_volterra_data_cleaned.csv` | Stores a processed dataset for analysis. |
| `models/lotka_volterra.py` | Simulates and plots the classical predator–prey model. |
| `models/sindy_model.py` | Fits a SINDy model and compares its simulated trajectories with the reference system. |
| `experiments/linearization.py` | Compares the nonlinear model with its linear approximation near equilibrium. |
| `experiments/error_analysis.py` | Reserved for error analysis and model evaluation. |
| `notebooks/data_analysis.ipynb` | Jupyter notebook for data exploration and analysis. |

## Installation

### Prerequisites

- Python 3.10 or a compatible Python version supported by your installed dependencies
- `pip`
- Jupyter Notebook or JupyterLab (optional, for notebook-based analysis)

### 1. Clone the repository

```bash
git clone https://github.com/troyc03/tchin-sindy-lotka-volterra.git
cd tchin-sindy-lotka-volterra
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it before installing dependencies.

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install numpy pandas scipy matplotlib pysindy jupyter
```

These packages support numerical computation, data handling, ODE integration, plotting, SINDy model fitting, and notebook-based analysis.

## Usage

Run the following commands from the repository root.

### Generate synthetic data

```bash
python data/generate.py
```

This simulates the system and writes the resulting dataset to:

```text
data/raw/lotka_volterra_data.csv
```

Running the generator again overwrites the existing raw CSV file.

### Simulate the Lotka–Volterra model

```bash
python models/lotka_volterra.py
```

This script plots the prey and predator populations over time and their phase-space trajectory.

### Fit the SINDy model

```bash
python models/sindy_model.py
```

This script simulates a reference system, fits a SINDy model using a quadratic polynomial feature library, prints the identified equations, and compares the reconstructed trajectories with the original populations.

### Compare nonlinear and linearized dynamics

```bash
python experiments/linearization.py
```

This script examines how a local linear approximation compares with the nonlinear system near its equilibrium point.

### Explore the notebook

Launch Jupyter from the repository root:

```bash
jupyter notebook
```

Open `notebooks/data_analysis.ipynb` to explore the data analysis workflow.

## Results and Evaluation

The main objective is to determine whether SINDy can recover a sparse representation of the Lotka–Volterra equations from sampled population trajectories.

Useful evaluation criteria include:

- **Equation recovery:** Whether the discovered terms match the known governing equations.
- **Coefficient accuracy:** How closely the identified coefficients match the reference parameters.
- **Trajectory agreement:** How closely the identified model reproduces the simulated population dynamics.
- **Noise sensitivity:** How measurement noise affects equation discovery and prediction.
- **Model sparsity:** Whether the algorithm identifies the essential terms without retaining unnecessary features.

For a quantitative evaluation, compare the identified coefficients with the known parameters and calculate trajectory errors over a defined prediction interval. Results should be reported from actual model runs rather than assumed in advance.

## Limitations

- The synthetic data are generated from a known mathematical model, so they do not represent the full complexity of real ecological systems.
- Numerical differentiation can introduce errors into derivative estimates.
- Noise, sampling frequency, feature-library selection, and sparsity thresholds can affect the discovered equations.
- A model that fits the training trajectory well may not generalize to different initial conditions or parameter regimes.
- The current scripts define their own simulation parameters; the data generator and SINDy demonstration should be checked for parameter consistency when comparing results.

## Future Work

Potential extensions include:

- Evaluate equation recovery across multiple noise levels.
- Quantify parameter and trajectory errors.
- Investigate the effects of sampling frequency and differentiation methods.
- Compare alternative SINDy optimizers and sparsity thresholds.
- Test the identified equations on trajectories generated from different initial conditions.
- Separate model training and evaluation data to assess generalization.
- Extend the workflow to experimental predator–prey data or other nonlinear dynamical systems.

## References

1. Brunton, S. L., Proctor, J. L., and Kutz, J. N. (2016). *Discovering governing equations from data by sparse identification of nonlinear dynamical systems.* Proceedings of the National Academy of Sciences, 113(15), 3932–3937. [https://doi.org/10.1073/pnas.1517384113](https://doi.org/10.1073/pnas.1517384113)
2. [PySINDy documentation](https://pysindy.readthedocs.io/)
3. [Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)

## License

This project is distributed under the GNU General Public License v3.0 (GPL-3.0). See [`LICENSE`](LICENSE) for details.
