# Setup Instructions
#
# Make environment variable PYTHONSTARTUP point to this file.
#
# TODO Refer to the following to improve this process:
# - https://stackoverflow.com/questions/11124578/automatically-import-modules-when-entering-the-python-or-ipython-interpreter
# - https://ipython.readthedocs.io/en/stable/config/intro.html


# System imports
from dotenv import load_dotenv
from panel import widgets
from panel.interact import interact
from panel.interact import interact, interactive, fixed, interact_manual
from pathlib import Path
from string import digits
import csv
import dateparser
import hvplot.pandas
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import panel as pn
import plotly.express as px
import sys


# Local imports
sys.path.append("../lib2")
from Constants import Constants
from MCForecastTools_Generic import MCSimulation_Generic
from PlotBuildingToools import PlotBuildingToools
from PreprocessingTools import CustomerNameCleaningFunctions
from PreprocessingTools import DateCleaningFunctions
from PreprocessingTools import DurationParsing
from PreprocessingTools import MappingFunctions
from PreprocessingTools import SpecializedDateCleaningFunctions
from ProcessingTools import DateProcessingTools


# Initialization Functions
def init_preprocessing(debug_level):
    
    pn.extension()

    # Construct the tools
    constants = Constants()
    tool_customer = CustomerNameCleaningFunctions(debug_level)
    tool_data_processing = DateProcessingTools(debug_level)
    tool_date = DateCleaningFunctions(debug_level)
    tool_duration_parsing = DurationParsing(debug_level)
    tool_lookup_tables = MappingFunctions(debug_level)
    tool_mapping = MappingFunctions(debug_level)
    tool_plot_building = PlotBuildingToools(debug_level)
    tool_special_date = SpecializedDateCleaningFunctions(debug_level)

    return {
        "constants": constants,
        "tool_customer": tool_customer,
        "tool_data_processing": tool_data_processing,
        "tool_date": tool_date,
        "tool_duration_parsing": tool_duration_parsing,
        "tool_lookup_tables": tool_lookup_tables,
        "tool_mapping": tool_mapping,
        "tool_plot_building": tool_plot_building,
        "tool_special_date": tool_special_date
    }

def init_processing(debug_level):
    
    pn.extension()

    # Construct the tools
    constants = Constants()
    tool_customer = CustomerNameCleaningFunctions(debug_level)
    tool_data_processing = DateProcessingTools(debug_level)
    tool_date = DateCleaningFunctions(debug_level)
    tool_duration_parsing = DurationParsing(debug_level)
    tool_lookup_tables = MappingFunctions(debug_level)
    tool_mapping = MappingFunctions(debug_level)
    tool_plot_building = PlotBuildingToools(debug_level)
    tool_special_date = SpecializedDateCleaningFunctions(debug_level)

    return {
        "constants": constants,
        "tool_customer": tool_customer,
        "tool_data_processing": tool_data_processing,
        "tool_date": tool_date,
        "tool_duration_parsing": tool_duration_parsing,
        "tool_lookup_tables": tool_lookup_tables,
        "tool_mapping": tool_mapping,
        "tool_plot_building": tool_plot_building,
        "tool_special_date": tool_special_date
    }
