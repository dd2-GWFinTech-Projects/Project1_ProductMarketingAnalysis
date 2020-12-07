# Setup Instructions
#
# Make environment variable PYTHONSTARTUP point to this file.
#
# TODO Refer to the following to improve this process:
# - https://stackoverflow.com/questions/11124578/automatically-import-modules-when-entering-the-python-or-ipython-interpreter
# - https://ipython.readthedocs.io/en/stable/config/intro.html

print("DEBUG")

# System imports
from dotenv import load_dotenv
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from panel import widgets
from panel.interact import interact
from panel.interact import interact, interactive, fixed, interact_manual
from pathlib import Path
from string import digits
import calendar
import csv
import dateparser
import enum
import holoviews as hv
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
from PlotBuildingTools import PlotBuildingTools
from PreprocessingTools import CustomerNameCleaningFunctions, DateCleaningFunctions, DurationParsing, SpecializedDateCleaningFunctions, MappingFunctions
from ProcessingTools import DateProcessingTools
# from UpgradeSequenceTools import UpgradeSequenceTool, UpgradeSequenceFilterTool, UpgradeSequenceReportTool




# Specialized imports
from UpgradeSequenceDataStructures import UpgradeType
from UpgradeSequenceDataStructures import CustomerBehaviorObservations
from UpgradeSequenceDataStructures import CustomerBehaviorClassifications

from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerBehaviorCounts
from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerAverageAnnualSales

from MCForecastTools_MacroCustomerSales import MacroCustomerSales_HistoricalAnalysis
from MCForecastTools_MacroCustomerSales import MacroCustomerSales_ForwardPredictor
from MCForecastTools_MacroCustomerSales import MacroCustomerSales_InstantaneousVariation
from MCForecastTools_MacroCustomerSales import MacroCustomerSales_MCSimulation












# Load extensions
# pn.extension()
pn.extension("plotly")
hv.extension('bokeh', 'matplotlib')


class Tools:
    def __init__(self, debug_level):
        # Construct the tools
        self.tool_customer = CustomerNameCleaningFunctions(debug_level)
        self.tool_data_processing = DateProcessingTools(debug_level)
        self.tool_date = DateCleaningFunctions(debug_level)
        self.tool_duration_parsing = DurationParsing(debug_level)
        self.tool_lookup_tables = MappingFunctions(debug_level)
        self.tool_mapping = MappingFunctions(debug_level)
        self.tool_plot_building = PlotBuildingTools(debug_level)
        self.tool_special_date = SpecializedDateCleaningFunctions(debug_level)
        # self.upgrade_sequence_tool = UpgradeSequenceTool(debug_level)
        # self.upgrade_sequence_filter_tool = UpgradeSequenceFilterTool(debug_level)
        # self.upgrade_sequence_report_tool = UpgradeSequenceReportTool(debug_level)
        self.tool_historical = MacroCustomerSales_HistoricalAnalysis()
        self.tool_fwd = MacroCustomerSales_ForwardPredictor()
        self.tool_inst = MacroCustomerSales_InstantaneousVariation()


# Initialization Functions

def init_preprocessing(debug_level):
    # pn.extension()
    return (Constants(), Tools(debug_level))

def init_processing(debug_level):
    # pn.extension()
    return (Constants(), Tools(debug_level))
