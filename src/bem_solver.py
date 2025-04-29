import numpy as np
from src.airfoil_tools import interpolate_airfoil_coefficients

def solve_bem(r, c, beta, af_id, v0, pitch, rpm, polar_database):
    """
    Solve BEM equations for thrust, torque, and power.
    
    Parameters:
    -----------
    r : array
        Blade span positions [m]
    c : array
        Chord lengths at each span position [m]
    beta : array
        Twist angles at each span position [deg]
    af_id : array
        Airfoil index at each span position
    v0 : float
        Inflow wind speed [m/s]
    pitch : float
        Blade pitch angle [deg]
    rpm : float
        Rotational speed [rpm]
    polar_database : dict
        Dictionary containing airfoil polars (alpha, cl, cd)
    
    Returns:
    --------
    T : float
        Thrust [N]
    M : float
        Torque [Nm]
    P : float
        Power [W]
    a : array
        Axial induction factors
    a_prime : array
        Tangential induction factors
    """
    rho = 1.225  # Air density [kg/m³]
    B = 3        # Number of blades
    R = np.max(r)
    omega = rpm * 2 * np.pi / 60  # Convert rpm to rad/s

    # Initialize induction factors
    a = np.zeros_like(r)
    a_prime = np.zeros_like(r)

    # Calculate element spacing (used for integration)
    dr = np.gradient(r)  # Proper spacing between span points

    # Iterate for each blade element
    for i in range(len(r)):
        # Skip elements with zero or very small radius (like at the hub)
        if r[i] < 0.01 * R:
            continue
            
        # Calculate local solidity
        sigma = (B * c[i]) / (2 * np.pi * r[i])
        
        # Iterative solution for induction factors
        for _ in range(100):  # Maximum 100 iterations
            # Flow angle
            phi = np.arctan2((1 - a[i]) * v0, (1 + a_prime[i]) * omega * r[i])
            
            # Angle of attack [deg]
            alpha = np.rad2deg(phi) - (pitch + beta[i])
            
            # Get airfoil data and interpolate coefficients
            if af_id[i] in polar_database:
                alpha_data, cl_data, cd_data = polar_database[af_id[i]]
                cl, cd = interpolate_airfoil_coefficients(alpha_data, cl_data, cd_data, alpha)
            else:
                # Use default values if airfoil data not available
                cl, cd = 0.0001, 0.35
            
            # Calculate normal and tangential force coefficients
            cn = cl * np.cos(phi) + cd * np.sin(phi)
            ct = cl * np.sin(phi) - cd * np.cos(phi)
            
            # Calculate new induction factors
            new_a = 1 / ((4 * np.sin(phi)**2) / (sigma * cn) + 1)
            
            # Avoid division by zero or negative values
            if ct <= 0 or np.sin(phi) == 0 or np.cos(phi) == 0:
                new_a_prime = 0
            else:
                new_a_prime = 1 / ((4 * np.sin(phi) * np.cos(phi)) / (sigma * ct) - 1)
            
            # Check for convergence
            if np.abs(new_a - a[i]) < 1e-5 and np.abs(new_a_prime - a_prime[i]) < 1e-5:
                break
                
            # Update induction factors with relaxation
            a[i] = 0.75 * a[i] + 0.25 * new_a
            a_prime[i] = 0.75 * a_prime[i] + 0.25 * new_a_prime
            
            # Ensure induction factors are within physical limits
            a[i] = np.clip(a[i], 0, 0.5)
            a_prime[i] = np.clip(a_prime[i], -0.5, 0.5)

    # Calculate elemental thrust and torque
    dT = 4 * np.pi * r * rho * v0**2 * a * (1 - a) * dr
    dM = 4 * np.pi * r**3 * rho * v0 * omega * a_prime * (1 - a) * dr

    # Integrate to get total thrust and torque
    T = np.sum(dT)  # Thrust [N]
    M = np.sum(dM)  # Torque [Nm]
    P = M * omega   # Power [W]

    return T, M, P, a, a_prime

def compute_power_thrust_curves(blade_data, operational_data, polar_database):
    """
    Computes the power and thrust curves for a range of wind speeds.
    
    Parameters:
    -----------
    blade_data : tuple
        Tuple containing (r, c, beta, af_id)
    operational_data : tuple
        Tuple containing (v0_array, pitch_array, rpm_array)
    polar_database : dict
        Dictionary containing airfoil polars
        
    Returns:
    --------
    v0_array : array
        Wind speeds [m/s]
    power_curve : array
        Power values [kW]
    thrust_curve : array
        Thrust values [kN]
    torque_curve : array
        Torque values [Nm]
    """
    r, c, beta, af_id = blade_data
    v0_array, pitch_array, rpm_array = operational_data

    power_curve = []
    thrust_curve = []
    torque_curve = []
    
    for v0, pitch, rpm in zip(v0_array, pitch_array, rpm_array):
        T, M, P, _, _ = solve_bem(r, c, beta, af_id, v0, pitch, rpm, polar_database)
        power_curve.append(P / 1000)  # Convert W to kW
        thrust_curve.append(T / 1000)  # Convert N to kN
        torque_curve.append(M)  # Nm
    
    return v0_array, power_curve, thrust_curve, torque_curve

def compute_cp_ct_surfaces(blade_data, polar_database, pitch_range, tsr_range, v0=10.0):
    """
    Compute power coefficient (Cp) and thrust coefficient (Ct) surfaces
    as a function of blade pitch angle and tip speed ratio.
    
    Parameters:
    -----------
    blade_data : tuple
        Tuple containing (r, c, beta, af_id)
    polar_database : dict
        Dictionary containing airfoil polars
    pitch_range : array
        Range of pitch angles to sweep [deg]
    tsr_range : array
        Range of tip speed ratios to sweep
    v0 : float, optional
        Reference wind speed [m/s]
        
    Returns:
    --------
    pitch_grid : 2D array
        Pitch angles for the surface [deg]
    tsr_grid : 2D array
        Tip speed ratios for the surface
    cp_surface : 2D array
        Power coefficient surface
    ct_surface : 2D array
        Thrust coefficient surface
    """
    r, c, beta, af_id = blade_data
    R = np.max(r)  # Rotor radius
    rho = 1.225    # Air density [kg/m³]
    A = np.pi * R**2  # Rotor area
    
    # Create meshgrid for pitch and TSR
    pitch_grid, tsr_grid = np.meshgrid(pitch_range, tsr_range)
    cp_surface = np.zeros_like(pitch_grid)
    ct_surface = np.zeros_like(pitch_grid)
    
    # Loop through all combinations
    for i in range(len(tsr_range)):
        for j in range(len(pitch_range)):
            tsr = tsr_grid[i, j]
            pitch = pitch_grid[i, j]
            
            # Calculate RPM from TSR
            rpm = (tsr * v0 * 60) / (2 * np.pi * R)
            
            # Solve BEM
            T, M, P, _, _ = solve_bem(r, c, beta, af_id, v0, pitch, rpm, polar_database)
            
            # Calculate coefficients
            cp = P / (0.5 * rho * A * v0**3)
            ct = T / (0.5 * rho * A * v0**2)
            
            # Store results
            cp_surface[i, j] = cp
            ct_surface[i, j] = ct
    
    return pitch_grid, tsr_grid, cp_surface, ct_surface