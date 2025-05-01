# tests/test_bem.py

import os
import numpy as np
import pytest
import matplotlib.pyplot as plt

from data_loader import load_blade_geometry, load_airfoil_polars, load_operational_strategy
from bem_solver import solve_bem, compute_power_thrust_curves
from performance_curves import plot_performance_curves, plot_operational_strategy, plot_cl_cd_vs_alpha
from airfoil_tools import interpolate_airfoil_coefficients

@pytest.fixture(scope="session")
def paths_and_data():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    blade_file = os.path.join(base, "inputs", "IEA-15-240-RWT", "IEA-15-240-RWT_AeroDyn15_blade.dat")
    polar_folder = os.path.join(base, "inputs", "IEA-15-240-RWT", "Airfoils")
    opt_file = os.path.join(base, "inputs", "IEA-15-240-RWT", "IEA_15MW_RWT_Onshore.opt")

    r, c, beta, af_id = load_blade_geometry(blade_file)
    polar_db = load_airfoil_polars(polar_folder)

    return {
        "r": r,
        "c": c,
        "beta": beta,
        "af_id": af_id,
        "polar_db": polar_db,
        "opt_file": opt_file,
    }


def test_load_blade_and_airfoil(paths_and_data):
    r = paths_and_data["r"]
    c = paths_and_data["c"]
    beta = paths_and_data["beta"]
    af_id = paths_and_data["af_id"]
    polar_db = paths_and_data["polar_db"]

    assert isinstance(r, np.ndarray)
    assert isinstance(c, np.ndarray)
    assert isinstance(beta, np.ndarray)
    assert r.shape == c.shape == beta.shape

    assert isinstance(af_id, np.ndarray) and af_id.size > 0
    assert isinstance(polar_db, dict) and polar_db


def test_interpolate_airfoil_coefficients(paths_and_data):
    r = paths_and_data["r"]
    af_id = paths_and_data["af_id"]
    polar_db = paths_and_data["polar_db"]

    idx = len(r) // 2
    key = af_id[idx]
    alpha, cl_vals, cd_vals = polar_db[key]

    cl, cd = interpolate_airfoil_coefficients(alpha, cl_vals, cd_vals, 5.0)

    assert isinstance(cl, float)
    assert isinstance(cd, float)
    assert cl >= 0 and cd >= 0


def test_solve_bem_and_physical_results(paths_and_data):
    r = paths_and_data["r"]
    c = paths_and_data["c"]
    beta = paths_and_data["beta"]
    af_id = paths_and_data["af_id"]
    polar_db = paths_and_data["polar_db"]

    T, M, P, a, a_prime = solve_bem(r, c, beta, af_id, 10.0, 0.0, 7.5, polar_db)

    assert T > 0
    assert M > 0
    assert P > 0
    assert np.all(a >= 0) and np.all(a <= 1)
    assert np.all(a_prime >= 0) and np.all(a_prime <= 1)


def test_load_operational_strategy(paths_and_data):
    v0, pitch, rpm, power_ref, thrust_ref = load_operational_strategy(paths_and_data["opt_file"])

    assert len(v0) == len(pitch) == len(rpm)
    assert len(power_ref) == len(thrust_ref)


def test_compute_power_thrust_curves(paths_and_data):
    r = paths_and_data["r"]
    c = paths_and_data["c"]
    beta = paths_and_data["beta"]
    af_id = paths_and_data["af_id"]
    polar_db = paths_and_data["polar_db"]

    v0, pitch, rpm, power_ref, thrust_ref = load_operational_strategy(paths_and_data["opt_file"])
    v0_out, P_curve, T_curve, Q_curve = compute_power_thrust_curves(
        (r, c, beta, af_id), (v0, pitch, rpm), polar_db
    )

    assert isinstance(v0_out, (list, np.ndarray))
    L = len(v0_out)
    assert len(P_curve) == len(T_curve) == len(Q_curve) == L


def test_plotting_functions_do_not_raise(paths_and_data, tmp_path):
    polar_db = paths_and_data["polar_db"]
    af_id = paths_and_data["af_id"]

    # plot_cl_cd_vs_alpha
    fig1 = plot_cl_cd_vs_alpha(polar_db, af_id[0])
    fig1.savefig(tmp_path / "cl_cd.png")
    plt.close(fig1)

    v0, pitch, rpm, power_ref, thrust_ref = load_operational_strategy(paths_and_data["opt_file"])
    fig2 = plot_operational_strategy(v0, pitch, rpm)
    fig2.savefig(tmp_path / "ops.png")
    plt.close(fig2)

    v0_out, P_curve, T_curve, Q_curve = compute_power_thrust_curves((
        paths_and_data["r"], paths_and_data["c"], paths_and_data["beta"], af_id
    ), (v0, pitch, rpm), polar_db)
    fig3 = plot_performance_curves(v0_out, P_curve, T_curve, power_ref, thrust_ref)
    fig3.savefig(tmp_path / "perf.png")
    plt.close(fig3)

    assert (tmp_path / "cl_cd.png").exists()
    assert (tmp_path / "ops.png").exists()
    assert (tmp_path / "perf.png").exists()
