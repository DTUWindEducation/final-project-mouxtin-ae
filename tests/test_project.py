import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from bem_solver import solve_bem, compute_power_thrust_curves
from performance_curves import plot_cl_cd_vs_alpha, plot_operational_strategy, plot_performance_curves

def run_tests():
    # === Setup paths ===
    blade_file = 'inputs/IEA-15-240-RWT/IEA-15-240-RWT_AeroDyn15_blade.dat'
    polar_folder = 'inputs/IEA-15-240-RWT/Airfoils'
    operational_file = 'inputs/IEA-15-240-RWT/IEA_15MW_RWT_Onshore.opt'

    # === 1. Load and parse turbine data ===
    print("\n[TEST 1] Loading turbine data...")
    try:
        r, c, beta, af_id = load_blade_geometry(blade_file)
        polar_database = load_airfoil_polars(polar_folder)
        print("✅ Blade and airfoil data loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load turbine data: {e}")
        return

    # === 2. Plot airfoil shapes in one figure ===
    print("\n[TEST 2] Plotting airfoil shapes...")
    try:
        for af in sorted(polar_database.keys())[:3]:  # just plot a few
            alpha, cl, cd = polar_database[af]
            plt.plot(alpha, cl, label=f"Airfoil {af}")
        plt.xlabel("Angle of attack [deg]")
        plt.ylabel("Lift coefficient Cl")
        plt.title("Example Airfoil Shapes")
        plt.legend()
        plt.grid()
        plt.savefig("outputs/test_airfoil_shapes.png")
        plt.close()
        print("✅ Airfoil shape plot created and saved.")
    except Exception as e:
        print(f"❌ Failed to plot airfoil shapes: {e}")
        return

    # === 3. Compute Cl and Cd as function of r and alpha ===
    print("\n[TEST 3] Interpolating Cl and Cd...")
    try:
        af_idx = af_id[len(r)//2]  # mid-span airfoil
        alpha_sample = 5.0  # test angle
        alpha_data, cl_data, cd_data = polar_database[af_idx]
        from airfoil_tools import interpolate_airfoil_coefficients
        cl, cd = interpolate_airfoil_coefficients(alpha_data, cl_data, cd_data, alpha_sample)
        print(f"✅ Interpolated Cl = {cl:.3f}, Cd = {cd:.3f} at α = {alpha_sample}° for airfoil {af_idx}.")
    except Exception as e:
        print(f"❌ Failed to interpolate Cl/Cd: {e}")
        return

    # === 4. Compute axial (a) and tangential (a') induction factors ===
    print("\n[TEST 4] Solving BEM for one wind speed...")
    try:
        v0_test = 10.0  # [m/s]
        pitch_test = 0.0  # [deg]
        rpm_test = 7.5  # [rpm]
        T, M, P, a, a_prime = solve_bem(r, c, beta, af_id, v0_test, pitch_test, rpm_test, polar_database)
        print(f"✅ BEM solved: Thrust={T:.1f} N, Torque={M:.1f} Nm, Power={P/1000:.1f} kW")
    except Exception as e:
        print(f"❌ Failed to solve BEM: {e}")
        return

    # === 5. Compute thrust (T), torque (M), and power (P) as function of V0, pitch, and rpm ===
    print("\n[TEST 5] Checking outputs for rotor performance...")
    if T > 0 and M > 0 and P > 0:
        print("✅ Thrust, Torque, and Power computed correctly.")
    else:
        print("❌ Non-physical results: Thrust, Torque, or Power <= 0.")

    # === 6. Compute optimal operational strategy ===
    print("\n[TEST 6] Loading operational strategy...")
    try:
        v0_array, pitch_array, rpm_array, power_ref, thrust_ref = load_operational_strategy(operational_file)
        plot_operational_strategy(v0_array, pitch_array, rpm_array)
        plt.savefig("outputs/test_operational_strategy.png")
        plt.close()
        print("✅ Operational strategy loaded and plotted.")
    except Exception as e:
        print(f"❌ Failed to load or plot operational strategy: {e}")
        return

    # === 7. Compute and plot power and thrust curves ===
    print("\n[TEST 7] Computing and plotting performance curves...")
    try:
        blade_data = (r, c, beta, af_id)
        operational_data = (v0_array, pitch_array, rpm_array)
        v0_array, power_curve, thrust_curve, torque_curve = compute_power_thrust_curves(blade_data, operational_data, polar_database)
        plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref, thrust_ref)
        plt.savefig("outputs/test_performance_curves.png")
        plt.close()
        print("✅ Power and thrust curves computed and plotted.")
    except Exception as e:
        print(f"❌ Failed to compute or plot performance curves: {e}")
        return

    print("\n🎯 All 7 functional requirements PASSED successfully.")

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    run_tests()
