import sys
import os
import matplotlib.pyplot as plt

# Ensure access to src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from src.bem_solver import solve_bem, compute_power_thrust_curves
from src.performance_curves import (
    plot_performance_curves,
    plot_spanwise_variables,
    plot_operational_strategy,
    plot_cl_cd_vs_alpha
)

# === Utility to auto-save all figures ===
def save_all_figures(output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    for i, fig in enumerate(plt.get_fignums()):
        plt.figure(fig)
        plt.savefig(os.path.join(output_dir, f"figure_{i+1}.png"), bbox_inches='tight')
        plt.savefig(os.path.join(output_dir, f"figure_{i+1}.pdf"), bbox_inches='tight')
    print(f"✅ All figures saved to '{output_dir}'.")

def main():
    # === Load data ===
    blade_file = 'inputs/IEA-15-240-RWT/IEA-15-240-RWT_AeroDyn15_blade.dat'
    polar_folder = 'inputs/IEA-15-240-RWT/Airfoils'
    operational_file = 'inputs/IEA-15-240-RWT/IEA_15MW_RWT_Onshore.opt'

    r, c, beta, af_id = load_blade_geometry(blade_file)
    polar_database = load_airfoil_polars(polar_folder)
    v0_array, pitch_array, rpm_array, power_ref, thrust_ref = load_operational_strategy(operational_file)

    # === Plot Cl/Cd vs α for an example airfoil ID ===
    plot_cl_cd_vs_alpha(polar_database, af_id_example=10)

    # === Plot operational strategy (pitch & RPM vs wind speed) ===
    plot_operational_strategy(v0_array, pitch_array, rpm_array)

    # === Compute performance curves ===
    v0_array, power_curve, thrust_curve, torque_curve = compute_power_thrust_curves(
        (r, c, beta, af_id),
        (v0_array, pitch_array, rpm_array),
        polar_database
    )

    plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref, thrust_ref)

    # === Solve BEM for one specific case ===
    case_idx = 10
    T, M, P, a, a_prime = solve_bem(
        r, c, beta, af_id,
        v0_array[case_idx],
        pitch_array[case_idx],
        rpm_array[case_idx],
        polar_database
    )

    print("=== Turbine performance at selected wind speed ===")
    print(f"Wind speed: {v0_array[case_idx]:.2f} m/s")
    print(f"Thrust: {T:.2f} N")
    print(f"Torque: {M:.2f} Nm")
    print(f"Power: {P/1000:.2f} kW")

    plot_spanwise_variables(r, a, a_prime, v0_array[case_idx], rpm_array[case_idx])

    # === Save all figures ===
    save_all_figures("outputs")

if __name__ == "__main__":
    main()
