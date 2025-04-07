"""
Tests for the wind turbine classes.
"""

import numpy as np
import pytest
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend to speed up tests

import sys
import os

# Add the src directory to the Python path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.wind_turbine.turbine_classes import GeneralWindTurbine, WindTurbine

# Small datasets for faster testing
SMALL_DATASET = np.array([
    [0.0, 0.0],
    [3.0, 0.0],
    [5.0, 250.0],
    [10.0, 1500.0],
    [12.0, 2000.0],
    [15.0, 2000.0],
    [25.0, 2000.0],
    [26.0, 0.0]
])


class TestGeneralWindTurbine:
    """Tests for the GeneralWindTurbine class."""
    
    @pytest.fixture
    def sample_turbine(self):
        """Create a sample wind turbine for testing."""
        return GeneralWindTurbine(
            rotor_diameter=100.0,
            hub_height=90.0,
            rated_power=2000.0,
            v_in=3.0,
            v_rated=12.0,
            v_out=25.0,
            name="Test Turbine"
        )
    
    def test_init(self, sample_turbine):
        """Test turbine initialization."""
        assert sample_turbine.rotor_diameter == 100.0
        assert sample_turbine.hub_height == 90.0
        assert sample_turbine.rated_power == 2000.0
        assert sample_turbine.v_in == 3.0
        assert sample_turbine.v_rated == 12.0
        assert sample_turbine.v_out == 25.0
        assert sample_turbine.name == "Test Turbine"
    
    def test_power_calculation(self, sample_turbine):
        """Test power calculations for key wind speeds."""
        # Below cut-in
        assert sample_turbine.get_power(2.0) == 0
        
        # Above cut-out
        assert sample_turbine.get_power(26.0) == 0
        
        # At rated wind speed
        assert sample_turbine.get_power(12.0) == 2000.0
        
        # In cubic region - single point test
        expected_power = 2000.0 * (6.0/12.0)**3
        assert sample_turbine.get_power(6.0) == pytest.approx(expected_power)
    
    def test_get_power_array(self, sample_turbine):
        """Test get_power with a small array input."""
        speeds = np.array([2.0, 6.0, 12.0, 20.0, 26.0])
        expected = np.array([
            0.0,  # Below cut-in
            2000.0 * (6.0/12.0)**3,  # Cubic region
            2000.0,  # At rated
            2000.0,  # Above rated but below cut-out
            0.0  # Above cut-out
        ])
        np.testing.assert_allclose(sample_turbine.get_power(speeds), expected)
    
    def test_plot_power_curve(self, sample_turbine):
        """Test that plot_power_curve method runs without error."""
        # Use a very small number of points to speed up the test
        v_range = np.linspace(0, 30, 10)
        fig, ax = sample_turbine.plot_power_curve(v_range)
        # Just verify objects are returned, no need to check details
        assert fig is not None
        assert ax is not None


class TestWindTurbine:
    """Tests for the WindTurbine class."""
    
    @pytest.fixture
    def sample_turbine(self):
        """Create a sample wind turbine with power curve for testing."""
        return WindTurbine(
            rotor_diameter=100.0,
            hub_height=90.0,
            rated_power=2000.0,
            v_in=3.0,
            v_rated=12.0,
            v_out=25.0,
            power_curve_data=SMALL_DATASET,
            name="Test Turbine"
        )
    
    def test_init(self, sample_turbine):
        """Test turbine initialization with power curve."""
        assert sample_turbine.rotor_diameter == 100.0
        assert sample_turbine.rated_power == 2000.0
        np.testing.assert_array_equal(sample_turbine.power_curve_data, SMALL_DATASET)
    
    def test_get_power_interpolation(self, sample_turbine):
        """Test power interpolation from the power curve."""
        # Test exact points from the dataset
        assert sample_turbine.get_power(3.0) == 0.0
        assert sample_turbine.get_power(12.0) == 2000.0
        
        # Test interpolated points
        assert sample_turbine.get_power(4.0) == pytest.approx(125.0)  # Between 3.0 and 5.0
        assert sample_turbine.get_power(11.0) == pytest.approx(1750.0)  # Between 10.0 and 12.0
    
    def test_get_power_out_of_range(self, sample_turbine):
        """Test power output for wind speeds outside the power curve range."""
        assert sample_turbine.get_power(0.0) == 0.0
        assert sample_turbine.get_power(30.0) == 0.0
    
    def test_get_power_array(self, sample_turbine):
        """Test get_power with a small array input."""
        speeds = np.array([2.0, 4.0, 12.0, 20.0, 30.0])
        expected = np.array([
            0.0,  # Below cut-in
            125.0,  # Interpolated value
            2000.0,  # At rated
            2000.0,  # Between rated and cut-out
            0.0  # Above cut-out
        ])
        np.testing.assert_allclose(sample_turbine.get_power(speeds), expected, rtol=1e-5)