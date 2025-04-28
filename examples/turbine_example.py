"""
Example script demonstrating the use of wind turbine classes.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

# Add the src directory to the Python path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.wind_turbine.turbine_classes import GeneralWindTurbine, WindTurbine

def main():
    """
    Main function to demonstrate wind turbine classes using LEANWIND_8MW_164_RWT data.
    """
    # LEANWIND_8MW_164_RWT turbine specifications
    rotor_diameter = 164.0  # m
    hub_height = 110.0  # m
    rated_power = 8000.0  # kW
    v_in = 4.0  # m/s
    v_rated = 12.5  # m/s
    v_out = 25.0  # m/s
    name = "LEANWIND_8MW_164_RWT"
    
    # Create a GeneralWindTurbine instance
    general_turbine = GeneralWindTurbine(
        rotor_diameter=rotor_diameter,
        hub_height=hub_height,
        rated_power=rated_power,
        v_in=v_in,
        v_rated=v_rated,
        v_out=v_out,
        name=f"{name} (Theoretical)"
    )
    
    # Load the power curve data
    try:
        # Try to load from URL (might require internet connection)
        url = "https://raw.githubusercontent.com/NREL/turbine-models/main/turbine_models/data/Offshore/LEANWIND_Reference_8MW_164.csv"
        power_curve_df = pd.read_csv(url)
        
        # Print column names to debug
        print("CSV columns:", power_curve_df.columns.tolist())
        
        # Use position-based indexing to be safe
        # First column is typically wind speed, second is power
        wind_speed = power_curve_df.iloc[:, 0].values
        power = power_curve_df.iloc[:, 1].values
        
        print(f"Wind speed range: {min(wind_speed)} to {max(wind_speed)} m/s")
        print(f"Power range: {min(power)} to {max(power)} kW")
        
        power_curve_data = np.column_stack((wind_speed, power))
        
        # Create a WindTurbine instance with the power curve data
        actual_turbine = WindTurbine(
            rotor_diameter=rotor_diameter,
            hub_height=hub_height,
            rated_power=rated_power,
            v_in=v_in,
            v_rated=v_rated,
            v_out=v_out,
            power_curve_data=power_curve_data,
            name=f"{name} (Actual)"
        )
        
        # Plot and compare power curves
        v_range = np.linspace(0, 30, 300)
        
        # Create a plot using the first turbine's method
        fig, ax = general_turbine.plot_power_curve(v_range)
        
        # Add the second turbine's power curve to the same plot
        power_actual = actual_turbine.get_power(v_range)
        ax.plot(v_range, power_actual, label=actual_turbine.name)
        
        # Enhance the plot
        ax.legend()
        ax.set_title(f"Power Curve Comparison for {name}")
        ax.set_xlim(0, 30)
        ax.set_ylim(0, rated_power * 1.1)
        
        # Save the figure
        plt.savefig(f"{name}_power_curve_comparison.png")
        plt.show()
        
        # Demonstrate the get_power method for specific wind speeds
        test_speeds = [3.0, 5.0, 10.0, 12.5, 15.0, 26.0]
        print("\nPower output comparison:")
        print(f"{'Wind Speed (m/s)':^15} | {'Theoretical (kW)':^20} | {'Actual (kW)':^20}")
        print("-" * 59)
        
        for speed in test_speeds:
            power_gen = general_turbine.get_power(speed)
            power_act = actual_turbine.get_power(speed)
            print(f"{speed:^15.1f} | {power_gen:^20.1f} | {power_act:^20.1f}")
            
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        print("Using theoretical turbine model only...")
        
        # Plot just the theoretical turbine
        v_range = np.linspace(0, 30, 300)
        fig, ax = general_turbine.plot_power_curve(v_range)
        ax.set_title(f"Theoretical Power Curve for {name}")
        ax.set_xlim(0, 30)
        ax.set_ylim(0, rated_power * 1.1)
        plt.savefig(f"{name}_theoretical_power_curve.png")
        plt.show()

if __name__ == "__main__":
    main()