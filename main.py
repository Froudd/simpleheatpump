"""
Author: Frederic Bless & Cecilia Dean
Date: September 2023
Project: OST-Heat Pump in Python
"""

# %%
# Imports
# ------------------------------------------

# Python functions
import matplotlib.pyplot as plt

# Own functions
try:
    from heatpumpmodel import heatpump
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.abspath(".."))
from heatpumpmodel import heatpump  
# %%
# Loading the data
# ------------------------------------------
filename = ".\heatpumpmodel\data\mydata.txt"

 
# %%
# Variables for the calculation
# ------------------------------------------------------------------

compressor_efficiency = 0.71


# %%
# Calculating the COP using a fit
# ------------------------------------------------------------------

source = 30
sink = 60
cop_fit = heatpump.cop_from_temperatures(temperature_hot = sink,temperature_cold = source)
print("The COP calculated using a simple fit give the following result {}, for a source temperature of {} and a sink temperature of {}.".format(cop_fit,source,sink))

# Try make a function to calculate the COP Carnot (see https://en.wikipedia.org/wiki/Coefficient_of_performance)
