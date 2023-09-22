"""
Author: Frederic Bless
Date: July 2023
Project: Brauhaus
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
from simulation_brauhaus import heatpump    
# %%
# Loading the data
# ------------------------------------------
filename = ".\simulation_brauhaus\data\data_brauhaus_01.csv"

headers,units,time,process_demand,process_temp,gas_price,electricity_price,hotsource_price,coldsource_price,hotsource_temp,coldsource_temp = data_processing.load_datas(filename=filename)
time_unit = data_processing.get_time_unit(headers=headers,units=units)
 
# %%
# Variables for the calculation
# ------------------------------------------------------------------

efficiency_boiler = 0.9


# %%
# Calculating the COP and the prices for the different heat sources
# ------------------------------------------------------------------

# with the cold heat source (cheaper)
#-------------
COP_coldsource = []
price_coldsource = []
price_gas = []
for hot_temp, cold_temp, process_need,source_price,el_price,g_price in zip(process_temp,coldsource_temp,process_demand,coldsource_price,electricity_price,gas_price):
    cop_calculated = heatpump.cop_from_temperatures(temperature_hot = hot_temp,temperature_cold = cold_temp)
    COP_coldsource.append(cop_calculated)
    price_coldsource.append(data_processing.price_calculation(process_demand = process_need,source_price=source_price ,electricity_price= el_price,cop=cop_calculated))
    price_gas.append(data_processing.gas_price_calculation(process_demand=process_need, gas_price= g_price, boiler_efficiency= efficiency_boiler))

# with the hot heat source (cheaper)
#-------------
COP_hotsource = []
price_hotsource = []
for hot_temp, cold_temp, process_need,source_price,el_price in zip(process_temp, hotsource_temp, process_demand, hotsource_price, electricity_price):
    cop_calculated = heatpump.cop_from_temperatures(temperature_hot = hot_temp,temperature_cold = cold_temp)
    COP_hotsource.append(cop_calculated)
    price_hotsource.append(data_processing.price_calculation(process_demand = process_need,source_price=source_price ,electricity_price= el_price,cop=cop_calculated))


# %%
# Efficiency
# ---------------------------
# This plot shows the COP of the heat pump depending on the heat source. Those values are calculated with a simple fit using the temperature lift.

plt.figure()
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= COP_coldsource, ylabel = "COP",titre = "Efficiency depending on the source")
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= COP_hotsource, ylabel = "COP",titre = "Efficiency depending on the source")
plt.legend(["cold source","hot source"])

# %%
# Process information
# ---------------------------
# This plot shows the temperature and the amount of steam the process.

data_processing.plot_demand(energy_demand=process_demand,demand_temperature = process_temp)

# %%
# Temperatures
# ---------------------------
# This plot shows the temperatures of heat sources.

plt.figure()
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= coldsource_temp, ylabel = "Temperature [°C]",titre = "Temperature of both sources")
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= hotsource_temp, ylabel = "Temperature [°C]",titre = "Temperature of both sources")
plt.legend(["cold source","hot source"])

# %%
# Cost comparison
# ---------------------------
# This plot shows the cost of the steam depending on the system used.

plt.figure()
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= price_coldsource, ylabel = "Price [CHF/h]",titre = "Cost comparison")
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= price_hotsource, ylabel = "Price [CHF/h]",titre = "Cost comparison")
data_processing.plot_bauhaus(time = time, time_unit = time_unit, data= price_gas, ylabel = "Price [CHF/h]",titre = "Cost comparison")
plt.legend(["cold source","hot source","gas"])

# ----------------
plt.show()

# %%
# Total cost comparison
# ---------------------------
# This part is the calculation of the total cost during the whole period

if time_unit == "h":
    model = "forward"
    print("Total cost using {} for the whole period is {:.0f} CHF".format("the HP with the cold source",data_processing.cost_whole_period(time= time, cost = price_coldsource, model = model)))
    print("Total cost using {} for the whole period is {:.0f} CHF".format("the HP with the hot source",data_processing.cost_whole_period(time= time, cost = price_hotsource, model = model)))
    print("Total cost using {} for the whole period is {:.0f} CHF".format("the gas boiler",data_processing.cost_whole_period(time= time, cost = price_gas, model = model)))
    print("Total duration was {} hours".format(time[-1]-time[0]))