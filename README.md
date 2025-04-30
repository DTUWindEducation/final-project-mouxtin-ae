# Wind Turbine Modeling Using Blade‑Element‑Momentum (BEM) Theory

This repository implements a steady‑state Blade‑Element‑Momentum (BEM) model to predict the aerodynamic performance of the IEA 15 MW offshore reference wind turbine. It computes power, thrust, and torque as functions of wind speed, rotor speed, and blade pitch.

---

## Quick Start

1. *Clone the repository*
   bash
   git clone https://github.com/YourOrg/final-project-mouxtin-ae.git
   cd final-project-mouxtin-ae
   

2. *Create and activate a virtual environment* (recommended)
   bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .\.venv\Scripts\activate  # Windows PowerShell
   

3. *Install dependencies and your package*
   bash
   pip install --upgrade pip
   pip install -e .
   

4. *Run the demonstration*
   bash
   python examples/main.py
   
   This will load inputs/, run the BEM solver over the provided operating strategy, and save figures to outputs/.

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
