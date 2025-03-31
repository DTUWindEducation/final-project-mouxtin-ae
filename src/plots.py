import os
import matplotlib.pyplot as plt

def load_airfoil_data(filepath):
    """
    Load polar data from a .dat file.
    Expected columns: AoA (deg), Cl, Cd, Cm.
    Lines starting with '#' or '!' are skipped.
    If a line has only three columns, Cm is set to None.
    """
    aoa, cl, cd, cm = [], [], [], []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comment lines starting with '#' or '!'
                if line and not (line.startswith("#") or line.startswith("!")):
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            a = float(parts[0])
                            c = float(parts[1])
                            d = float(parts[2])
                            # If there is a fourth value, use it for Cm, else use None.
                            if len(parts) >= 4:
                                m = float(parts[3])
                            else:
                                m = None
                            aoa.append(a)
                            cl.append(c)
                            cd.append(d)
                            cm.append(m)
                        except ValueError:
                            continue  # Skip lines that don't convert properly
        print(f"Loaded {len(aoa)} data points from {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
    return aoa, cl, cd, cm

def load_coords(filepath):
    """
    Load airfoil coordinate data from a .txt file.
    Expected columns: x/c and y/c.
    Lines starting with '!' are skipped.
    """
    x_coords, y_coords = [], []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("!"):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            x = float(parts[0])
                            y = float(parts[1])
                            x_coords.append(x)
                            y_coords.append(y)
                        except ValueError:
                            continue
        print(f"Loaded {len(x_coords)} coordinate points from {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
    return x_coords, y_coords

def plot_polar_data(base_path, polar_pattern="IEA-15-240-RWT_AeroDyn15_Polar_{:02d}.dat", start=0, end=50):
    """
    Plot polar data from files with indices from start to end-1.
    Produces three separate figures:
      - Figure 1: Cl vs AoA (saved as 'polar_Cl.png')
      - Figure 2: Cd vs AoA (saved as 'polar_Cd.png')
      - Figure 3: Cm vs AoA (saved as 'polar_Cm.png')
    Each curve is labeled with its file index.
    """
    # Figure 1: Cl vs AoA
    plt.figure(figsize=(10, 6))
    for i in range(start, end):
        file_path = os.path.join(base_path, "Airfoils", polar_pattern.format(i))
        if os.path.exists(file_path):
            aoa, cl, _, _ = load_airfoil_data(file_path)
            if len(aoa) == len(cl) and len(aoa) > 0:
                plt.plot(aoa, cl, label=f"{i:02d}")
            else:
                print(f"Warning: Inconsistent data in {os.path.basename(file_path)}")
        else:
            print(f"File not found: {file_path}")
    plt.xlabel("Angle of Attack (°)")
    plt.ylabel("Lift Coefficient (Cl)")
    plt.title("Cl vs AoA from Polar Files")
    plt.legend(fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    cl_plot_filename = os.path.join(os.getcwd(), "polar_Cl.png")
    plt.savefig(cl_plot_filename)
    print(f"Saved Cl vs AoA plot as {cl_plot_filename}")
    plt.show()

    # Figure 2: Cd vs AoA
    plt.figure(figsize=(10, 6))
    for i in range(start, end):
        file_path = os.path.join(base_path, "Airfoils", polar_pattern.format(i))
        if os.path.exists(file_path):
            aoa, _, cd, _ = load_airfoil_data(file_path)
            if len(aoa) == len(cd) and len(aoa) > 0:
                plt.plot(aoa, cd, label=f"{i:02d}")
            else:
                print(f"Warning: Inconsistent data in {os.path.basename(file_path)}")
        else:
            print(f"File not found: {file_path}")
    plt.xlabel("Angle of Attack (°)")
    plt.ylabel("Drag Coefficient (Cd)")
    plt.title("Cd vs AoA from Polar Files")
    plt.legend(fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    cd_plot_filename = os.path.join(os.getcwd(), "polar_Cd.png")
    plt.savefig(cd_plot_filename)
    print(f"Saved Cd vs AoA plot as {cd_plot_filename}")
    plt.show()

    # Figure 3: Cm vs AoA
    plt.figure(figsize=(10, 6))
    for i in range(start, end):
        file_path = os.path.join(base_path, "Airfoils", polar_pattern.format(i))
        if os.path.exists(file_path):
            aoa, _, _, cm = load_airfoil_data(file_path)
            # Only plot if Cm values are not None and data lengths match.
            if len(aoa) == len(cm) and len(aoa) > 0 and all(m is not None for m in cm):
                plt.plot(aoa, cm, label=f"{i:02d}")
            else:
                print(f"Warning: Inconsistent or missing Cm data in {os.path.basename(file_path)}")
        else:
            print(f"File not found: {file_path}")
    plt.xlabel("Angle of Attack (°)")
    plt.ylabel("Moment Coefficient (Cm)")
    plt.title("Cm vs AoA from Polar Files")
    plt.legend(fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    cm_plot_filename = os.path.join(os.getcwd(), "polar_Cm.png")
    plt.savefig(cm_plot_filename)
    print(f"Saved Cm vs AoA plot as {cm_plot_filename}")
    plt.show()

def plot_coords_data(base_path, coords_pattern="IEA-15-240-RWT_AF{:02d}_Coords.txt", start=0, end=50):
    """
    Plot airfoil coordinate data from files with indices from start to end-1.
    Produces a single figure showing x/c vs y/c for all files (saved as 'airfoil_shapes.png').
    Each airfoil shape is labeled by its file index.
    """
    plt.figure(figsize=(10, 6))
    for i in range(start, end):
        file_path = os.path.join(base_path, "Airfoils", coords_pattern.format(i))
        if os.path.exists(file_path):
            x, y = load_coords(file_path)
            if len(x) > 0 and len(x) == len(y):
                plt.plot(x, y, label=f"{i:02d}")
            else:
                print(f"Warning: Inconsistent coordinate data in {os.path.basename(file_path)}")
        else:
            print(f"File not found: {file_path}")
    plt.xlabel("x/c")
    plt.ylabel("y/c")
    plt.title("Airfoil Shapes from Coordinate Files")
    plt.legend(fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    coords_plot_filename = os.path.join(os.getcwd(), "airfoil_shapes.png")
    plt.savefig(coords_plot_filename)
    print(f"Saved airfoil shapes plot as {coords_plot_filename}")
    plt.show()

if __name__ == "__main__":
    # Set the base path to the folder that contains "Airfoils".
    # For example, for Windows: C:\git\final-project-mouxtin-ae\inputs\IEA-15-240-RWT
    base_path = os.path.join("..", "inputs", "IEA-15-240-RWT")

    # Plot polar data (files indexed 0 to 49)
    plot_polar_data(base_path, start=0, end=50)

    # Plot coordinate data (files indexed 0 to 49)
    plot_coords_data(base_path, start=0, end=50)
