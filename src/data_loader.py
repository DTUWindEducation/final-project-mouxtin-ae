import numpy as np
import os
import glob

def load_blade_geometry(filepath):
    """
    Load blade geometry from IEA-15-240-RWT_AeroDyn15_blade.dat
    Returns span (r), chord (c), twist (beta), and airfoil id (af_id)
    """
    # Skip the header lines
    data = np.loadtxt(filepath, skiprows=8)

    r = data[:, 0]     # Blade span [m]
    c = data[:, 5]     # Chord [m]
    beta = data[:, 4]  # Twist angle [deg]
    af_id = data[:, 6].astype(int)  # Airfoil index

    return r, c, beta, af_id

def load_airfoil_polars(airfoil_folder):
    """
    Load all airfoil polar files into a dictionary.
    Keys are airfoil indices, values are (alpha, Cl, Cd) arrays.
    """
    polar_database = {}
    
    # Find all polar files in the folder
    polar_files = glob.glob(os.path.join(airfoil_folder, "*Polar*.dat"))
    
    for filepath in polar_files:
        # Extract the airfoil index from the filename
        filename = os.path.basename(filepath)
        af_idx_str = filename.split("_")[-1].split(".")[0]
        af_idx = int(af_idx_str) + 1  # Convert to 1-based index to match BlAFID
        
        # Read file manually
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Skip header lines and find the aerodynamic coefficients table
        data_lines = []
        in_table = False
        for line in lines:
            if "!    Alpha      Cl      Cd" in line:
                in_table = True
                continue
            if in_table and not line.strip().startswith('!'):
                data_lines.append(line)
        
        # Parse the data
        data = np.loadtxt(data_lines)
        alpha = data[:, 0]  # Angle of attack [deg]
        cl = data[:, 1]     # Lift coefficient
        cd = data[:, 2]     # Drag coefficient
        
        polar_database[af_idx] = (alpha, cl, cd)
    
    return polar_database

def load_airfoil_coordinates(airfoil_folder):
    """
    Load all airfoil coordinate files into a dictionary.
    Keys are airfoil indices, values are (x, y) coordinate arrays.
    """
    coords_database = {}
    
    # Find all coordinate files in the folder
    coord_files = glob.glob(os.path.join(airfoil_folder, "*Coords*.txt"))
    
    for filepath in coord_files:
        # Extract the airfoil index from the filename
        filename = os.path.basename(filepath)
        # Extract the number between "AF" and "_Coords"
        af_idx_str = filename.split("_AF")[1].split("_")[0]
        af_idx = int(af_idx_str) + 1  # Convert to 1-based index to match BlAFID
        
        # Skip header lines and find coordinates
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Skip to the actual coordinates
        data_lines = []
        for i, line in enumerate(lines):
            if "!  x/c        y/c" in line and i > 10:  # Skip reference point
                coord_start = i + 1
                break
        
        # Parse coordinate data
        data = np.loadtxt(lines[coord_start:])
        x = data[:, 0]  # Normalized x-coordinate
        y = data[:, 1]  # Normalized y-coordinate
        
        coords_database[af_idx] = (x, y)
    
    return coords_database

def load_operational_strategy(filepath):
    """
    Load wind speed, pitch angle, and RPM from operational file.
    """
    data = np.loadtxt(filepath, skiprows=1)
    v0 = data[:, 0]    # Wind speed [m/s]
    pitch = data[:, 1] # Blade pitch angle [deg]
    rpm = data[:, 2]   # Rotational speed [rpm]
    power = data[:, 3] # Power [kW]
    thrust = data[:, 4] # Thrust [kN]
    
    return v0, pitch, rpm, power, thrust