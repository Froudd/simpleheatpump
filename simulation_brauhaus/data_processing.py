"""
Reading data for the brauhaus project
"""
# Copyright (C) 2023 OST Ostschweizer Fachhochschule
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Author: Frederic Bless <frederic.bless@ost.ch>

import csv
import matplotlib.pyplot as plt
# import os

def load_data(
    *, filename: str ) -> list:
    """reading the data.

    Parameters
    ----------
    filename:
        name of the data file
    Returns
    -------
    load_data:
        list containing the hourly data.
    """
    data = []
    # print(filename)
    # print(os.getcwd())
    try:
        with open(filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)
            next(reader, None)
            for row in reader:
                data.append(float(row[1]))
    except:
        data = None 
    return data


def load_datas(
    *, filename: str ) -> list:
    """reading the datas from a csv file.

    Parameters
    ----------
    filename:
        name of the data file
    Returns
    -------
    load_datas:
        tuple of list containing the hourly datas.
    """
    data = []
    # print(filename)
    # print(os.getcwd())
    time = []
    header = []
    units = []
    process_demand = []
    process_temp = []
    gas_price = []
    electricity_price = []
    hotsource_price = []
    coldsource_price = []
    hotsource_temp = []
    coldsource_temp = []
    try:
        with open(filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader, None)
            units = next(reader, None)
            for row in reader:
                time.append(float(row[0]))
                process_demand.append(float(row[1]))
                process_temp.append(float(row[2]))
                gas_price.append(float(row[3]))
                electricity_price.append(float(row[4]))
                hotsource_price.append(float(row[5]))
                coldsource_price.append(float(row[6]))
                hotsource_temp.append(float(row[7]))
                coldsource_temp.append(float(row[8]))
    except:
        process_demand = None
        process_temp = None
        gas_price = None
        electricity_price = None
        hotsource_price = None
        coldsource_price = None
        hotsource_temp = None
        coldsource_temp = None
    return header,units,time,process_demand,process_temp,gas_price,electricity_price,hotsource_price,coldsource_price,hotsource_temp,coldsource_temp

def get_time_unit(
    *, headers: list, units: list ) -> str:
    """getting the time unit

    Parameters
    ----------
    headers:
        list containing the strings of the headers
    units:
        list containing the strings of the units
    Returns
    -------
    get_time_unit:
        get the unit of the time
    """
    unit = "h"
    index = 0
    for i,header in enumerate(headers):
        if "time" in header.lower():
            index = i
            break
    unit = units[index]
    return unit


def plot_cop(
    *, cop: list ):
    """plot the COP.

    Parameters
    ----------
    cop:
       cop as a list
    Returns
    -------
    None:
        plot the cop
    """
    plt.plot(cop)
    plt.ylabel("COP")
    plt.xlabel("time [h]")


def plot_price(
    *, price: list ):
    """plot the price.

    Parameters
    ----------
    price:
       price as a list

    Returns
    -------
    None:
        plot the price
    """
    plt.plot(price)
    plt.ylabel("price [CHF]")
    plt.xlabel("time [h]")


def plot_temperature(
    *, temperature: list ):
    """plot the temperature.

    Parameters
    ----------
    temperature:
       temperature as a list

    Returns
    -------
    None:
        plot the price
    """
    plt.plot(temperature)
    plt.ylabel("Temperature [°C]")
    plt.xlabel("time [h]")

def plot_bauhaus(
    *, time: list, time_unit: str, data: list, ylabel: str = "y-label",titre: str = " "):
    """plot the COP.

    Parameters
    ----------
    time:
       time used as the x-axis
    time_unit:
        the unit of time as a string
    data:
        the data to plot as a list
    ylabel:
        the title of the y label as a string
    titre:
        the title of the figure

    Returns
    -------
    None:
        plot the cop
    """
    plt.title(titre)
    plt.plot(time,data)
    plt.ylabel(ylabel)
    plt.xlabel("time [{}]".format(time_unit))

def plot_demand(
    *, energy_demand: list, demand_temperature: list):
    """plot the demand.

    Parameters
    ----------
    energy_demand:
       Energy demand as a list
    demand_temperature:
        Temperature of the steam as a list
    
    Returns
    -------
    None:
        plot the demand
    """
    # Creating plot with dataset_1
    fig, ax1 = plt.subplots()
    ax1.set_title("Process information")
    color = 'tab:red'
    ax1.set_xlabel('time [h]')
    ax1.set_ylabel('Heat demand [kW]', color = color)
    ax1.plot(energy_demand, color = color)
    ax1.tick_params(axis ='y', labelcolor = color)
    # Adding Twin Axes to plot using dataset_2
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Temperature demand [°C]', color = color)
    ax2.plot(demand_temperature, color = color)
    ax2.tick_params(axis ='y', labelcolor = color)


def price_calculation(
    *, process_demand: float, source_price: float , electricity_price: float, cop: float) -> float:
    """calculating the total cost of the steam
    cost = (demand/COP) * electricity_price + (demand-(demand/COP)) * source_price

    Parameters
    ----------
    process_demand:
        process demand in kWh
    source_price:
        price of the source in CHF/kWh
    electricity_price:
        electricity price in CHF/kWh
    cop:
        Coefficient of performance
    Returns
    -------
    price_calculation:
        price using a fit and the temperature lift
    """
    cost = (process_demand/cop) * electricity_price + (process_demand-(process_demand/cop)) * source_price
    return cost

def gas_price_calculation(
    *, process_demand: float, gas_price: float, boiler_efficiency: float = 0.9) -> float:
    """calculating the cost of the steam
    cost = (demand/boiler_efficiency) * gas_price

    Parameters
    ----------
    process_demand:
        process demand in kWh
    gas_price:
        price of the gas in CHF/kWh
    boiler_efficiency:
        efficiency of the boiler
    Returns
    -------
    gas_price_calculation:
        cost using the demand process, the efficiency, and the gas price
    """
    cost = (process_demand/boiler_efficiency) * gas_price
    return cost


def cost_whole_period(
    *, time: list, cost: list, model: str = "forward") -> float:
    """calculating the cost of the steam
    total_cost = time * cost

    Parameters
    ----------
    time:
        time
    cost:
        cost 
    model:
        model to do the calculation either "forward", "backward", or "average". Default is "forward".
    Returns
    -------
    cost_whole_period
        cost using the time and the value to calculate
    """
    cost_period = 0
    for i in range(0,len(time)-1,1):
        cost_period += cost[i]*(time[i+1]-time[i])
        # print("forward, cost: {}".format(cost_period))
    if model == "backward":
        # print("backward model used")
        cost_period = 0
        for i in range(1,len(time),1):
            cost_period += cost[i]*(time[i]-time[i-1])
    elif model == "average":
        # print("average model used")
        cost_period = 0
        for i in range(0,len(time)-1,1):
            cost_period += (cost[i+1] + cost[i])/2*(time[i+1]-time[i])

    return cost_period