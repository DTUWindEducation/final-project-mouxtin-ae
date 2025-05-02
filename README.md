# Wind Turbine Modeling Using Blade‑Element‑Momentum (BEM) Theory

# **Team**: Mouxtin A.E

## **Overview**
This repository implements a steady‑state Blade‑Element‑Momentum (BEM) model to predict the aerodynamic performance of a reference IEA 15 MW offshore wind turbine. It computes power, thrust, and torque as functions of wind speed, rotor speed, and blade pitch. The model simulates he aerodynamic performance of a horizontal-axis wind turbine. The BEM formulation combines momentum theory and blade element theory to iteratively solve for the axial and tangential induction factors \( a \) and \( a' \), which modify the local inflow velocity experienced by the blade elements.

The aerodynamic forces are computed using lift and drag coefficients $c_l$ and $C_d$, interpolated from airfoil polars as functions of the angle of attack $\alpha$. These are used to calculate the normal and tangential force coefficients:

```math
C_n = C_l \cos\phi + C_d \sin\phi, \quad
C_t = C_l \sin\phi - C_d \cos\phi
```

With these, the induction factors are updated using:

```math
a = \frac{1}{\left( \frac{4 \sin^2 \phi}{\sigma(r) C_n} + 1 \right)}, \quad
a' = \frac{1}{\left( \frac{4 \sin \phi \cos \phi}{\sigma(r) C_t} - 1 \right)}
```

Once convergence is achieved, the distributed loads are integrated over the blade span to yield total thrust \( T \), torque \( M \), and power \( P \):

```math
P = M \omega, \quad
C_P = \frac{P}{\frac{1}{2} \rho A V_0^3}, \quad
C_T = \frac{T}{\frac{1}{2} \rho A V_0^2}
```

The goal is to provide a computational tool for evaluating performance metrics as functions of inflow wind speed $V_0$, rotor speed $\omega$, and blade pitch angle $\theta_p$, enabling aerodynamic analysis and operational optimization of large-scale wind turbines.


---

## **Quick Start Guide**
To set up and run the simulation, follow these steps:

### **1️. Clone the Repository somewhere**
```sh
git clone https://github.com/DTUWindEducation/final-project-mouxtin-ae.git
```
```sh
cd final-project-mouxtin-ae
```
Ensure you have Python 3.11+:
```sh
python --version
```
<!-- ```sh
conda create -n windsim python=3.11 -y
conda activate windsim
pip install -r requirements.txt
``` -->

### **2. Set Up Virtual Environment (recommended)**
```sh
python3 -m venv .venv
```
```sh
source .venv/bin/activate   # Mac/Linux(GitBash)
```
```sh
source .venv/Scripts/activate # Windows Terminal
```
```sh
.\.venv\Scripts\Activate.ps1 # Windows PowerShell
```

### **3. Install dependencies of the package**
```sh
pip install --upgrade pip
```
```sh
pip install -e .[dev]
```
   

### **4. Run the package**
```sh
   python examples/main.py
```
   This will load inputs/, run the BEM solver and save figures to outputs/.

---

## Project Structure

```text
final-project-mouxtin-ae/
├── inputs/                      # Provided turbine geometry, polars & strategy
├── outputs/                     # Generated performance figures (not pushed)
├── src/
│   └── bem_turbine/             # Installable BEM package
│       ├── data_loader.py       # parsing blade & strategy files
│       ├── airfoil.py           # airfoil shape & polar interpolation
│       ├── solver.py            # BEM induction‐factor solver
│       ├── performance.py       # power, thrust, torque computations
│       ├── plotting.py          # all plotting utilities
│       └── utils.py             # misc helper functions
├── tests/                       # pytest scripts, mirroring src modules
├── examples/
│   └── main.py                  # demo script that runs in <10 min
├── docs/                        # static diagrams and reference images
├── .gitignore
├── LICENSE
├── Collaboration.md             # team collaboration plan
├── README.md                    # this document
└── pyproject.toml               # project metadata & dependencies
```


---

## Installation

Ensure Python 3.10+ is installed. Then:
bash
pip install -e .

This installs the bem_turbine package in editable mode and pulls in any requirements listed in pyproject.toml.

---

## Architecture Overview

We follow the 4+1 view model in miniature:

- *Logical (Functionality):* The bem_turbine package provides classes/functions to load input data, solve the BEM equations, and post-process results.
- *Development (Module Structure):* All code resides under src/bem_turbine with one module per major responsibility.
- *Process (Performance):* The solver vectorizes operations over blade elements; plotting routines produce figures in under 10 min on a typical laptop.
- *Physical (Deployment):* Installation via pip install -e .; no external data files are needed beyond inputs/.
- *Use‐Case (Examples):* examples/main.py demonstrates a full run from inputs → outputs.

A UML‐style block diagram (in docs/figures/rotor_diagram.jpeg) illustrates the data flow: inputs → BEM solver → performance curves → plots.

---

## Functional Requirements

The package implements all mandated functions:

1. *Data loading & parsing* (data_loader.py).
2. *Airfoil shape plotting* (plotting.py: plot_all_airfoil_shapes).
3. *Lift/drag vs span & angle-of-attack* (plotting.py: plot_cl_cd_vs_r_alpha).
4. *Induction factors a, a′ vs span* (solver.py: solve_bem).
5. *Power, thrust, torque vs wind speed* (performance.py: compute_power_thrust_curves).
6. *Operational strategy plotting* (plotting.py: plot_operational_strategy).
7. *Reference vs computed performance curves* (plotting.py: plot_performance_curves).

Additional helper functions in utils.py extend the feature set.

---

## Examples

examples/main.py illustrates:

- Loading blade geometry & polars.
- Solving BEM over the given wind‐speed array.
- Plotting and saving:
  - Airfoil shapes.
  - Cl/Cd vs α for sample stations.
  - Spanwise induction factors.
  - Power, thrust, torque curves vs wind speed.
  - Operational strategy (pitch & RPM).

Figures are written to outputs/ as both PNG and PDF.

---

## Testing & Quality

- *Tests:* Each module in src/bem_turbine has a corresponding test in tests/, ensuring ≥ 80% coverage (pytest --cov=src tests/).
- *Linting:* Pylint score maintained at ≥ 8.0 (pylint src/bem_turbine).
- *CI:* GitHub Actions runs tests and style checks on every PR.

---

## Team Collaboration

See [Collaboration.md](Collaboration.md) for detailed roles, workflow, and communication channels.

---

## References & Further Reading

- Hansen, M.O.L. (2015). Aerodynamics of Wind Turbines, 3rd ed.
- IEC 61400‑1: Wind turbine design requirements.
- Gaertner et al. (2020). IEA 15 MW offshore reference turbine, NREL/TP‑5000.

Additional resources and background are listed in the course slides and README templates under docs.

---
