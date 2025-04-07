# Wind Turbine Classes

This package provides classes for modeling wind turbine power output based on wind speed.

## Classes

- `GeneralWindTurbine`: A theoretical model using the cubic power curve equation
- `WindTurbine`: A data-driven model using actual power curve data and interpolation

## Features

- Calculate power output for any wind speed
- Compare theoretical and actual power curves
- Support for both scalar and array inputs
- Visualization of power curves

## Installation

To install this package in development mode:

```bash
pip install -e .