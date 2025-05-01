import os
import numpy as np
import pytest
import matplotlib.pyplot as plt

from data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from bem_solver import solve_bem, compute_power_thrust_curves
from performance_curves import plot_cl_cd_vs_alpha, plot_operational_strategy, plot_performance_curves
from airfoil_tools import interpolate_airfoil_coefficients

# --- Fixtures for input paths and loaded data --------------------------------
@pytest.fixture(scope="session")
def paths_and_data():
    # Base project directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    blade_file = os.path.join(base_dir, 'inputs', 'IEA-15-240-RWT',
                              'IEA-15-240-RWT_AeroDyn15_blade.dat')
    polar_folder = os.path.join(base_dir, 'inputs', 'IEA-15-240-RWT', 'Airfoils')
    operational_file = os.path.join(base_dir, 'inputs', 'IEA-15-240-RWT',
                                    'IEA_15MW_RWT_Onshore.opt')

    # Load geometry and polars once
    r, c, beta, af_id = load_blade_geometry(blade_file)
    polar_db = load_airfoil_polars(polar_folder)

    return {
        'r': r,
        'c': c,
        'beta': beta,
        'af_id': af_id,
        'polar_db': polar_db,
        'operational_file': operational_file
    }

# --- Tests ------------------------------------------------------------------

def test_load_blade_and_airfoil(paths_and_data):
    r = paths_and_data['r']
    c = paths_and_data['c']
    beta = paths_and_data['beta']
    af_id = paths_and_data['af_id']
    polar_db = paths_and_data['polar_db']

    assert isinstance(r, np.ndarray)
    assert isinstance(c, np.ndarray)
    assert isinstance(beta, np.ndarray)
    assert r.shape == c.shape == beta.shape
    assert isinstance(af_id, dict) and af_id
    assert isinstance(polar_db, dict) and polar_db, "Polar database should not be empty"


def test_interpolate_airfoil_coefficients(paths_and_data):
    r = paths_and_data['r']
    af_id = paths_and_data['af_id']
    polar_db = paths_and_data['polar_db']

    mid_idx = len(r) // 2
    af_key = af_id[mid_idx]
    alpha, cl_vals, cd_vals = polar_db[af_key]

    # sample interpolation
    cl, cd = interpolate_airfoil_coefficients(alpha, cl_vals, cd_vals, alpha_sample=5.0)

    assert isinstance(cl, float)
    assert isinstance(cd, float)
    assert cl >= 0 and cd >= 0


def test_solve_bem_and_physical_results(paths_and_data):
    r = paths_and_data['r']
    c = paths_and_data['c']
    beta = paths_and_data['beta']
    af_id = paths_and_data['af_id']
    polar_db = paths_and_data['polar_db']

    # Solve BEM at a representative condition
    T, M, P, a, a_prime = solve_bem(r, c, beta, af_id,
                                     v0=10.0, pitch=0.0, rpm=7.5,
                                     polar_db=polar_db)

    assert T > 0, "Thrust should be positive"
    assert M > 0, "Torque should be positive"
    assert P > 0, "Power should be positive"
    # Induction factors between 0 and 1
    assert np.all(a >= 0) and np.all(a <= 1)
    assert np.all(a_prime >= 0) and np.all(a_prime <= 1)


def test_load_operational_strategy(paths_and_data):
    operational_file = paths_and_data['operational_file']
    v0_arr, pitch_arr, rpm_arr, power_ref, thrust_ref = \
        load_operational_strategy(operational_file)

    # Check lengths match
    assert len(v0_arr) == len(pitch_arr) == len(rpm_arr)
    assert len(power_ref) == len(thrust_ref)


def test_compute_power_thrust_curves(paths_and_data):
    r = paths_and_data['r']
    c = paths_and_data['c']
    beta = paths_and_data['beta']
    af_id = paths_and_data['af_id']
    polar_db = paths_and_data['polar_db']
    operational_file = paths_and_data['operational_file']

    # reload operational arrays
    v0_arr, pitch_arr, rpm_arr, power_ref, thrust_ref = \
        load_operational_strategy(operational_file)

    v0_out, P_curve, T_curve, Q_curve = compute_power_thrust_curves(
        (r, c, beta, af_id), (v0_arr, pitch_arr, rpm_arr), polar_db)

    # consistency checks
    assert isinstance(v0_out, np.ndarray)
    assert v0_out.shape == P_curve.shape == T_curve.shape == Q_curve.shape


def test_plotting_functions_do_not_raise(paths_and_data, tmp_path):
    # Verify that plotting utilities run without errors and can save files
    polar_db = paths_and_data['polar_db']
    operational_file = paths_and_data['operational_file']
    r = paths_and_data['r']
    c = paths_and_data['c']
    beta = paths_and_data['beta']
    af_id = paths_and_data['af_id']

    # pick a single airfoil
    alpha, cl_vals, cd_vals = next(iter(polar_db.values()))
    fig1 = plot_cl_cd_vs_alpha(alpha, cl_vals, cd_vals)
    fig1.savefig(tmp_path / 'cl_cd.png')
    plt.close(fig1)

    v0_arr, pitch_arr, rpm_arr, power_ref, thrust_ref = \
        load_operational_strategy(operational_file)
    fig2 = plot_operational_strategy(v0_arr, pitch_arr, rpm_arr)
    fig2.savefig(tmp_path / 'ops.png')
    plt.close(fig2)

    fig3 = plot_performance_curves(v0_out, P_curve, T_curve, power_ref, thrust_ref)
    fig3.savefig(tmp_path / 'perf.png')
    plt.close(fig3)

    # ensure files exist
    assert (tmp_path / 'cl_cd.png').exists()
    assert (tmp_path / 'ops.png').exists()
    assert (tmp_path / 'perf.png').exists()
