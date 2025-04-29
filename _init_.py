import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add the project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Import from src package
from src.data_loader import load_blade_geometry, load_airfoil_polars, load_airfoil_coordinates, load_operational_strategy
from src.airfoil_tools import plot_airfoil_shapes, plot_airfoil_polars
from src.bem_solver import solve_bem, compute_power_thrust_curves, compute_cp_ct_surfaces

def plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref=None, thrust_ref=None, figsize=(12, 8)):
    """
    Plot the power and thrust curves.
    
    Parameters:
    -----------
    v0_array : array
        Wind speeds [m/s]
    power_curve : array
        Power values [kW]
    thrust_curve : array
        Thrust values [kN]
    power_ref : array, optional
        Reference power values for comparison [kW]
    thrust_ref : array, optional
        Reference thrust values for comparison [kN]
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    fig : matplotlib figure
        The figure with power and thrust curves
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Plot power curve
    ax1.plot(v0_array, power_curve, 'b-', linewidth=2, label='BEM Prediction')
    if power_ref is not None:
        ax1.plot(v0_array, power_ref, 'r--', linewidth=2, label='Reference')
    
    ax1.set_xlabel('Wind Speed [m/s]')
    ax1.set_ylabel('Power [kW]')
    ax1.set_title('Power Curve')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # Plot thrust curve
    ax2.plot(v0_array, thrust_curve, 'g-', linewidth=2, label='BEM Prediction')
    if thrust_ref is not None:
        ax2.plot(v0_array, thrust_ref, 'r--', linewidth=2, label='Reference')
    
    ax2.set_xlabel('Wind Speed [m/s]')
    ax2.set_ylabel('Thrust [kN]')
    ax2.set_title('Thrust Curve')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    plt.tight_layout()
    return fig

def plot_cp_ct_surfaces(pitch_grid, tsr_grid, cp_surface, ct_surface, figsize=(14, 6)):
    """
    Plot the power coefficient (Cp) and thrust coefficient (Ct) surfaces.
    
    Parameters:
    -----------
    pitch_grid : 2D array
        Pitch angles for the surface [deg]
    tsr_grid : 2D array
        Tip speed ratios for the surface
    cp_surface : 2D array
        Power coefficient surface
    ct_surface : 2D array
        Thrust coefficient surface
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    fig : matplotlib figure
        The figure with Cp and Ct surfaces
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Plot Cp surface
    cp_levels = np.linspace(0, np.max(cp_surface), 20)
    cp_contour = ax1.contourf(pitch_grid, tsr_grid, cp_surface, levels=cp_levels, cmap='viridis')
    
    ax1.set_xlabel('Pitch Angle [deg]')
    ax1.set_ylabel('Tip Speed Ratio [-]')
    ax1.set_title('Power Coefficient (Cp)')
    fig.colorbar(cp_contour, ax=ax1, label='Cp [-]')
    
    # Plot Ct surface
    ct_levels = np.linspace(0, np.max(ct_surface), 20)
    ct_contour = ax2.contourf(pitch_grid, tsr_grid, ct_surface, levels=ct_levels, cmap='plasma')
    
    ax2.set_xlabel('Pitch Angle [deg]')
    ax2.set_ylabel('Tip Speed Ratio [-]')
    ax2.set_title('Thrust Coefficient (Ct)')
    fig.colorbar(ct_contour, ax=ax2, label='Ct [-]')
    
    plt.tight_layout()
    return fig

def plot_spanwise_variables(r, a, a_prime, v0, rpm, figsize=(10, 8)):
    """
    Plot spanwise distribution of induction factors and other variables.
    
    Parameters:
    -----------
    r : array
        Blade span positions [m]
    a : array
        Axial induction factors
    a_prime : array
        Tangential induction factors
    v0 : float
        Wind speed [m/s]
    rpm : float
        Rotor speed [rpm]
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    fig : matplotlib figure
        The figure with spanwise distributions
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Plot axial induction factor
    ax1.plot(r, a, 'b-', linewidth=2)
    ax1.set_xlabel('Blade Span [m]')
    ax1.set_ylabel('Axial Induction Factor (a)')
    ax1.set_title(f'Spanwise Axial Induction Distribution (V0={v0} m/s, RPM={rpm})')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xlim([r.min(), r.max()])
    
    # Plot tangential induction factor
    ax2.plot(r, a_prime, 'r-', linewidth=2)
    ax2.set_xlabel('Blade Span [m]')
    ax2.set_ylabel('Tangential Induction Factor (a\')')
    ax2.set_title(f'Spanwise Tangential Induction Distribution (V0={v0} m/s, RPM={rpm})')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xlim([r.min(), r.max()])
    
    plt.tight_layout()
    return fig

def plot_spanwise_forces(r, dT, dM, v0, rpm, figsize=(10, 8)):
    """
    Plot spanwise distribution of thrust and torque.
    
    Parameters:
    -----------
    r : array
        Blade span positions [m]
    dT : array
        Differential thrust [N/m]
    dM : array
        Differential torque [Nm/m]
    v0 : float
        Wind speed [m/s]
    rpm : float
        Rotor speed [rpm]
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    fig : matplotlib figure
        The figure with spanwise force distributions
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Plot differential thrust
    ax1.plot(r, dT, 'b-', linewidth=2)
    ax1.set_xlabel('Blade Span [m]')
    ax1.set_ylabel('dT/dr [N/m]')
    ax1.set_title(f'Spanwise Thrust Distribution (V0={v0} m/s, RPM={rpm})')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xlim([r.min(), r.max()])
    
    # Plot differential torque
    ax2.plot(r, dM, 'r-', linewidth=2)
    ax2.set_xlabel('Blade Span [m]')
    ax2.set_ylabel('dM/dr [Nm/m]')
    ax2.set_title(f'Spanwise Torque Distribution (V0={v0} m/s, RPM={rpm})')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xlim([r.min(), r.max()])
    
    plt.tight_layout()
    return fig

def calculate_aep(v0_array, power_curve, wind_dist, rated_power=15000):
    """
    Calculate Annual Energy Production (AEP) based on power curve and wind distribution.
    
    Parameters:
    -----------
    v0_array : array
        Wind speeds [m/s]
    power_curve : array
        Power values [kW]
    wind_dist : array
        Wind speed distribution (probability density) [-]
    rated_power : float, optional
        Rated power [kW]
        
    Returns:
    --------
    aep : float
        Annual Energy Production [GWh]
    cf : float
        Capacity factor [-]
    """
    # Make sure wind_dist is normalized
    wind_dist = wind_dist / np.sum(wind_dist)
    
    # Calculate power produced at each wind speed
    power_produced = np.array(power_curve) * wind_dist * 8760  # 8760 hours in a year
    
    # Sum to get total annual energy production
    aep = np.sum(power_produced) / 1000  # Convert MWh to GWh
    
    # Calculate capacity factor
    cf = aep / (rated_power * 8.760)  # 8.760 = 8760/1000 for GWh
    
    return aep, cf

def weibull_distribution(v, A=8.0, k=2.0):
    """
    Weibull probability density function for wind speed.
    
    Parameters:
    -----------
    v : array-like
        Wind speeds [m/s]
    A : float
        Scale parameter [m/s]
    k : float
        Shape parameter
        
    Returns:
    --------
    p : array-like
        Probability density
    """
    p = (k/A) * (v/A)**(k-1) * np.exp(-(v/A)**k)
    return p

def main():
    # Define paths
    input_dir = os.path.join(project_root, 'inputs', 'IEA-15-240-RWT')
    blade_file = os.path.join(input_dir, 'IEA-15-240-RWT_AeroDyn15_blade.dat')
    operational_file = os.path.join(input_dir, 'IEA_15MW_RWT_Onshore.opt')
    airfoil_dir = os.path.join(input_dir, 'Airfoils')
    
    # 1. Load blade geometry
    print("Loading blade geometry...")
    r, c, beta, af_id = load_blade_geometry(blade_file)
    
    # 2. Load airfoil data
    print("Loading airfoil data...")
    polar_database = load_airfoil_polars(airfoil_dir)
    coords_database = load_airfoil_coordinates(airfoil_dir)
    
    # 3. Load operational strategy
    print("Loading operational strategy...")
    v0_ref, pitch_ref, rpm_ref, power_ref, thrust_ref = load_operational_strategy(operational_file)
    
    # 4. Plot airfoil shapes
    print("Plotting airfoil shapes...")
    fig_shapes = plot_airfoil_shapes(coords_database)
    fig_shapes.savefig(os.path.join(project_root, 'results', 'airfoil_shapes.png'))
    
    # 5. Plot airfoil polars for selected airfoils
    print("Plotting airfoil polars...")
    selected_airfoils = [1, 10, 20, 30, 40, 50]  # Example selection
    fig_polars = plot_airfoil_polars(polar_database, selected_airfoils)
    fig_polars.savefig(os.path.join(project_root, 'results', 'airfoil_polars.png'))
    
    # 6. Compute power and thrust curves using reference operational data
    print("Computing power and thrust curves...")
    blade_data = (r, c, beta, af_id)
    operational_data = (v0_ref, pitch_ref, rpm_ref)
    v0_array, power_curve, thrust_curve, torque_curve = compute_power_thrust_curves(blade_data, operational_data, polar_database)
    
    # 7. Plot power and thrust curves
    print("Plotting performance curves...")
    fig_perf = plot_performance_curves(v0_array, power_curve, thrust_curve, power_ref, thrust_ref)
    fig_perf.savefig(os.path.join(project_root, 'results', 'performance_curves.png'))
    
    # 8. Compute Cp-Ct surfaces
    print("Computing Cp-Ct surfaces...")
    pitch_range = np.linspace(0, 20, 21)
    tsr_range = np.linspace(4, 12, 17)
    pitch_grid, tsr_grid, cp_surface, ct_surface = compute_cp_ct_surfaces(blade_data, polar_database, pitch_range, tsr_range)
    
    # 9. Plot Cp-Ct surfaces
    print("Plotting Cp-Ct surfaces...")
    fig_cp_ct = plot_cp_ct_surfaces(pitch_grid, tsr_grid, cp_surface, ct_surface)
    fig_cp_ct.savefig(os.path.join(project_root, 'results', 'cp_ct_surfaces.png'))
    
    # 10. Calculate induction factors for a specific operating point
    print("Calculating spanwise distributions...")
    v0 = 10.0  # Example wind speed
    pitch = pitch_ref[np.where(v0_ref == v0)[0][0]]
    rpm = rpm_ref[np.where(v0_ref == v0)[0][0]]
    
    T, M, P, a, a_prime = solve_bem(r, c, beta, af_id, v0, pitch, rpm, polar_database)
    
    # 11. Plot spanwise variables
    print("Plotting spanwise variables...")
    fig_spanwise = plot_spanwise_variables(r, a, a_prime, v0, rpm)
    fig_spanwise.savefig(os.path.join(project_root, 'results', 'spanwise_variables.png'))
    
    # 12. Calculate AEP using Weibull distribution
    print("Calculating Annual Energy Production...")
    wind_dist = weibull_distribution(v0_array)
    aep, cf = calculate_aep(v0_array, power_curve, wind_dist)
    print(f"Annual Energy Production: {aep:.2f} GWh")
    print(f"Capacity Factor: {cf:.4f}")
    
    print("All calculations completed successfully!")

if __name__ == "__main__":
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    main()