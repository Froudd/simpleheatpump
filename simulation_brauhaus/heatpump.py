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

def cop_from_temperatures(
    *, temperature_hot: float, temperature_cold: float , t_pinch_hot: float = 5, t_pinch_cold: float = 5 ) -> float:
    """reading the data.
    COP=52.94∙Δ𝑇^-0.716 with R2=0.8826
    
    Parameters
    ----------
    temperature_hot:
        temperature hot in °C
    temperature_cold:
        temperature cold in °C
    t_pinch_hot:
        pinch temperature in the hot each exchanger in °C
    t_pinch_cold:
        pinch temperature in the cold each exchanger in °C
    Returns
    -------
    cop_from_temperatures:
        COP using a fit and the temperature lift
    """
    DeltaT = (temperature_hot - t_pinch_hot) - (temperature_cold + t_pinch_cold)
    cop = 52.94*pow(DeltaT,-0.716)
    return cop

