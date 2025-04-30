import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from src.bem_solver import solve_bem, compute_power_thrust_curves
from src.performance_curves import (
    plot_performance_curves,
    plot_spanwise_variables,
    plot_operational_strategy,
    plot_cl_cd_vs_alpha
)
from plots import plot_coords_data, plot_polar_data

def main():
    base_path = os.path.join("inputs", "IEA-15-240-RWT")
    blade_file = os.path.join(base_path, "IEA-15-240-RWT_AeroDyn15_blade.dat")
    polar_folder = os.path.join(base_path, "Airfoils")
    operational_file = os.path.join(base_path, "IEA_15MW_RWT_Onshore.opt")
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    print("📊 Generating airfoil shape and polar plots...")
    plot_coords_data(base_path, output_dir, start=0, end=50)
    plot_polar_data(base_path, output_dir, start=0, end=50)

    r, c, beta, af_id = load_blade_geometry(blade_file)
    polar_database = load_airfoil_polars(polar_folder)
    v0_array, pitch_array, rpm_array, power_ref, thrust_ref = load_operational_strategy(operational_file)

    fig3 = plot_cl_cd_vs_alpha(polar_database, af_id_example=10)
    fig3.savefig(os.path.join(output_dir, "cl_cd_vs_alpha_af10.jpg"), dpi=300, bbox_inches="tight")

    fig4 = plot_operational_strategy(v0_array, pitch_array, rpm_array)
    fig4.savefig(os.path.join(output_dir, "operational_strategy.jpg"), dpi=300, bbox_inches="tight")

    v0_array, power_curve, thrust_curve, torque_curve = compute_power_thrust_curves(
        (r, c, beta, af_id),
        (v0_array, pitch_array, rpm_array),
        polar_database
    )

    fig5 = plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref, thrust_ref)
    fig5.savefig(os.path.join(output_dir, "power_thrust_curves.jpg"), dpi=300, bbox_inches="tight")

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
    print(f"Power: {P / 1000:.2f} kW")

    fig6 = plot_spanwise_variables(r, a, a_prime, v0_array[case_idx], rpm_array[case_idx])
    fig6.savefig(os.path.join(output_dir, "spanwise_induction.jpg"), dpi=300, bbox_inches="tight")

    print("✅ All figures saved in 'outputs/' as .jpg")

if __name__ == "__main__":
    main()
