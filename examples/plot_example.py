"""
Evaluation simulation data
============================

This script simulated the cost of producing steam with three different possibilities. 
1) using gas and a steam gas boiler,
2) using a heat pump with the heating network inlet hot temperature as a source
3) using a heat pump with the heating network return line with a lower temperature as a source

The calculation are explained by the following shema:

.. figure:: ../_static/Simulation_flowshart.jpg
    :scale: 50%
   
    Flowschart of the simulation
"""

# %%
# Imports
# ------------------------------------------

# Python functions
import matplotlib.pyplot as plt

# Own functions
try:
    from simulation_brauhaus import data_processing
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.abspath(".."))
    from simulation_brauhaus import data_processing
from simulation_brauhaus import heatpump    
# %%
# Loading the data
# ------------------------------------------

filename1 = "..\simulation_brauhaus\data\hot_source_temperature.csv"
filename2 = "..\simulation_brauhaus\data\hot_source_price.csv"
filename3 = "..\simulation_brauhaus\data\cold_source_price.csv"
filename4 = "..\simulation_brauhaus\data\cold_source_temperature.csv"
filename5 = "..\simulation_brauhaus\data\electricity_price.csv"
filename6 = "..\simulation_brauhaus\data\process_demand.csv"
filename7 = "..\simulation_brauhaus\data\process_temperature.csv"
filename8 = "..\simulation_brauhaus\data\gas_price.csv"
hotsource_temp = data_processing.load_data(filename=filename1)
hotsource_price = data_processing.load_data(filename=filename2)
coldsource_price = data_processing.load_data(filename=filename3)
coldsource_temp = data_processing.load_data(filename=filename4)
electricity_price = data_processing.load_data(filename=filename5)
process_demand = data_processing.load_data(filename=filename6)
process_temp = data_processing.load_data(filename=filename7)
gas_price = data_processing.load_data(filename=filename8)



# %%
# Variables for the calculation
# ------------------------------------------------------------------

efficiency_boiler = 0.9

# %%
# Temperatures
# ---------------------------
# This plot shows the temperatures of heat sources.

plt.figure()
plt.title("Temperature")
data_processing.plot_temperature(temperature = coldsource_temp)
data_processing.plot_temperature(temperature = hotsource_temp)
plt.legend(["cold source","hot source"])

# %%
# Calculating the COP and the prices for the different heat sources
# ------------------------------------------------------------------

# with the cold heat source (cheaper)
#-------------
COP_coldsource = []
steam_price_coldsource = []
steam_price_gas = []
for hot_temp, cold_temp, process_need,source_price,el_price,g_price in zip(process_temp,coldsource_temp,process_demand,coldsource_price,electricity_price,gas_price):
    cop_calculated = heatpump.cop_from_temperatures(temperature_hot = hot_temp,temperature_cold = cold_temp)
    COP_coldsource.append(cop_calculated)
    steam_price_coldsource.append(data_processing.price_calculation(process_demand = process_need,source_price=source_price ,electricity_price= el_price,cop=cop_calculated))
    steam_price_gas.append(data_processing.gas_price_calculation(process_demand=process_need, gas_price= g_price, boiler_efficiency= efficiency_boiler))


# with the hot heat source (cheaper)
#-------------
COP_hotsource = []
steam_price_hotsource = []
for hot_temp, cold_temp, process_need,source_price,el_price in zip(process_temp, hotsource_temp, process_demand, hotsource_price, electricity_price):
    cop_calculated = heatpump.cop_from_temperatures(temperature_hot = hot_temp,temperature_cold = cold_temp)
    COP_hotsource.append(cop_calculated)
    steam_price_hotsource.append(data_processing.price_calculation(process_demand = process_need,source_price=source_price ,electricity_price= el_price,cop=cop_calculated))


# %%
# Efficiency
# ---------------------------
# This plot shows the COP of the heat pump depending on the heat source. Those values are calculated with a simple fit using the temperature lift.

plt.figure()
plt.title("Efficiency")
data_processing.plot_cop(cop=COP_coldsource)
data_processing.plot_cop(cop=COP_hotsource)
plt.legend(["cold source","hot source"])

# %%
# Process information
# ---------------------------
# This plot shows the temperature and the amount of steam the process.

data_processing.plot_demand(energy_demand=process_demand,demand_temperature = process_temp)

# %%
# Energy Prices
# ---------------------------
# This plot shows the cost of the energy that the heating system will used.

plt.figure()
plt.title("Energy cost")
data_processing.plot_price(price=coldsource_price)
data_processing.plot_price(price=hotsource_price)
data_processing.plot_price(price = gas_price)
data_processing.plot_price(price = electricity_price)
plt.legend(["cold source","hot source","gas","electricity"])
# %%
# Cost comparison
# ---------------------------
# This plot shows the cost of the steam depending on the system used.

plt.figure()
plt.title("Steam cost comparison")
data_processing.plot_price(price=steam_price_coldsource)
data_processing.plot_price(price=steam_price_hotsource)
data_processing.plot_price(price = steam_price_gas)
plt.legend(["cold source","hot source","gas"])

plt.show()

# %%
# Daily costs
# ---------------------------
# Adding the cost for the day
print("The total cost per day is {:.0f} CHF for the heat pump using the cold source, {:.0f} CHF for heat pump using the hot source, and {:.0f} for the gas boiler.".format(sum(steam_price_coldsource),sum(steam_price_hotsource),sum(steam_price_gas)))
