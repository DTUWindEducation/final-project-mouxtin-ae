"""Main execution script for wind turbine BEM model analysis."""
import os
import matplotlib.pyplot as plt


from piwe_bem_mouxtin_ae.data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from piwe_bem_mouxtin_ae.bem_solver import solve_bem, compute_power_thrust_curves
from piwe_bem_mouxtin_ae.performance_curves import (
    plot_performance_curves,
    plot_spanwise_variables,
    plot_operational_strategy,
    plot_cl_cd_vs_alpha_all
)
from piwe_bem_mouxtin_ae.plots import plot_coords_data, plot_polar_data

def main():
    base_path = os.path.join("inputs", "IEA-15-240-RWT")
    blade_file = os.path.join(base_path, "IEA-15-240-RWT_AeroDyn15_blade.dat")
    polar_folder = os.path.join(base_path, "Airfoils")
    operational_file = os.path.join(base_path, "IEA_15MW_RWT_Onshore.opt")
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    plot_coords_data(base_path, output_dir, start=0, end=50)
    plot_polar_data(base_path, output_dir, start=0, end=50)

    r, c, beta, af_id = load_blade_geometry(blade_file)
    polar_database = load_airfoil_polars(polar_folder)
    v0_array, pitch_array, rpm_array, power_ref, thrust_ref = load_operational_strategy(operational_file)

    plot_cl_cd_vs_alpha_all(polar_database, output_dir)

    fig_strategy = plot_operational_strategy(v0_array, pitch_array, rpm_array)
    fig_strategy.savefig(os.path.join(output_dir, "operational_strategy.jpg"), dpi=300, bbox_inches="tight")

    v0_array, power_curve, thrust_curve, _ = compute_power_thrust_curves(
        (r, c, beta, af_id),
        (v0_array, pitch_array, rpm_array),
        polar_database
    )

    fig_perf = plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref, thrust_ref)
    fig_perf.savefig(os.path.join(output_dir, "power_thrust_curves.jpg"), dpi=300, bbox_inches="tight")

    case_idx = 10
    T, M, P, a, a_prime = solve_bem(
        r, c, beta, af_id,
        v0_array[case_idx],
        pitch_array[case_idx],
        rpm_array[case_idx],
        polar_database
    )

    print("=== Turbine performance ===")
    print(f"Wind speed: {v0_array[case_idx]:.2f} m/s")
    print(f"Thrust: {T:.2f} N")
    print(f"Torque: {M:.2f} Nm")
    print(f"Power: {P / 1000:.2f} kW")

    fig_span = plot_spanwise_variables(r, a, a_prime, v0_array[case_idx], rpm_array[case_idx])
    fig_span.savefig(os.path.join(output_dir, "spanwise_induction.jpg"), dpi=300, bbox_inches="tight")

    print("All figures saved in 'outputs/'")

if __name__ == "__main__":
    main()
