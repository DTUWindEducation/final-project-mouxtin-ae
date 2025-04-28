"""
Wind Turbine classes for modeling power output based on wind speed.
"""

import numpy as np
import matplotlib.pyplot as plt


class GeneralWindTurbine:
    """
    A general wind turbine class that calculates power output based on theoretical power curve.
    
    Attributes:
        rotor_diameter (float): Rotor diameter in meters
        hub_height (float): Hub height in meters
        rated_power (float): Rated power in kilowatts
        v_in (float): Cut-in wind speed in m/s
        v_rated (float): Rated wind speed in m/s
        v_out (float): Cut-out wind speed in m/s
        name (str, optional): Name of the turbine
    """
    
    def __init__(self, rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, name=None):
        """
        Initialize a general wind turbine with theoretical power curve.
        
        Args:
            rotor_diameter (float): Rotor diameter in meters
            hub_height (float): Hub height in meters
            rated_power (float): Rated power in kilowatts
            v_in (float): Cut-in wind speed in m/s
            v_rated (float): Rated wind speed in m/s
            v_out (float): Cut-out wind speed in m/s
            name (str, optional): Name of the turbine. Defaults to None.
        """
        self.rotor_diameter = rotor_diameter
        self.hub_height = hub_height
        self.rated_power = rated_power
        self.v_in = v_in
        self.v_rated = v_rated
        self.v_out = v_out
        self.name = name
    
    def get_power(self, v):
        """
        Calculate power output for a given wind speed.
        
        Args:
            v (float or array-like): Wind speed in m/s
            
        Returns:
            float or array-like: Power output in kilowatts
        """
        # Handle numpy arrays and scalar values
        if isinstance(v, (list, np.ndarray)):
            return np.array([self._calc_power(speed) for speed in v])
        else:
            return self._calc_power(v)
    
    def _calc_power(self, v):
        """
        Helper method to calculate power for a single wind speed value.
        
        Args:
            v (float): Wind speed in m/s
            
        Returns:
            float: Power output in kilowatts
        """
        if v < self.v_in or v > self.v_out:
            return 0
        elif v < self.v_rated:
            return self.rated_power * (v / self.v_rated) ** 3
        else:
            return self.rated_power
    
    def plot_power_curve(self, v_range=None, label=None):
        """
        Plot the power curve for this turbine.
        
        Args:
            v_range (array-like, optional): Range of wind speeds to plot. Defaults to None.
            label (str, optional): Label for the plot legend. Defaults to turbine name.
            
        Returns:
            tuple: Figure and axis objects
        """
        if v_range is None:
            v_range = np.linspace(0, self.v_out + 2, 100)
        
        power = self.get_power(v_range)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(v_range, power, label=label or self.name or "Theoretical")
        ax.set_xlabel("Wind Speed (m/s)")
        ax.set_ylabel("Power (kW)")
        ax.set_title("Wind Turbine Power Curve")
        ax.grid(True)
        if label or self.name:
            ax.legend()
        
        return fig, ax


class WindTurbine(GeneralWindTurbine):
    """
    A wind turbine class that uses actual power curve data for calculating power output.
    
    Attributes:
        power_curve_data (numpy.ndarray): Array with shape (n, 2) containing wind speed and power data
        All attributes from GeneralWindTurbine
    """
    
    def __init__(self, rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, 
                 power_curve_data, name=None):
        """
        Initialize a wind turbine with actual power curve data.
        
        Args:
            rotor_diameter (float): Rotor diameter in meters
            hub_height (float): Hub height in meters
            rated_power (float): Rated power in kilowatts
            v_in (float): Cut-in wind speed in m/s
            v_rated (float): Rated wind speed in m/s
            v_out (float): Cut-out wind speed in m/s
            power_curve_data (array-like): Array with shape (n, 2) containing wind speed and power data
            name (str, optional): Name of the turbine. Defaults to None.
        """
        super().__init__(rotor_diameter, hub_height, rated_power, v_in, v_rated, v_out, name)
        self.power_curve_data = np.array(power_curve_data)
    
    def get_power(self, v):
        """
        Calculate power output for a given wind speed using interpolation on the power curve data.
        
        Args:
            v (float or array-like): Wind speed in m/s
            
        Returns:
            float or array-like: Power output in kilowatts
        """
        # Extract wind speeds and power values from the power curve data
        wind_speeds = self.power_curve_data[:, 0]
        power_values = self.power_curve_data[:, 1]
        
        # Handle values outside the range of the power curve data
        v_min = np.min(wind_speeds)
        v_max = np.max(wind_speeds)
        
        # Use numpy's interp function for both scalar and array inputs
        if isinstance(v, (list, np.ndarray)):
            result = np.zeros_like(v, dtype=float)
            valid_indices = (v >= v_min) & (v <= v_max)
            result[valid_indices] = np.interp(v[valid_indices], wind_speeds, power_values)
            return result
        else:
            if v < v_min or v > v_max:
                return 0
            return np.interp(v, wind_speeds, power_values)