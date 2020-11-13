# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
# System imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import hvplot.pandas
import panel as pn
from pathlib import Path
from panel.interact import interact
from panel import widgets
from string import digits
import csv
import json
import numpy as np
import dateparser
import panel as pn

pn.extension()



# %%
# Local imports
import sys
sys.path.append("Projects/Project8-david/lib2/")

from Constants import Constants
from ProcessingTools import DateProcessingTools
from MCForecastTools_Generic import MCSimulation_Generic


# %%
# Construct the tools
debug_level = 0
constants = Constants()
tool_data_processing = DateProcessingTools(debug_level)


# %%
# Import all preprocessed data
atlas           = pd.read_pickle(constants.PREPROCESSED_ATLAS_FILE_PATH)
forecast        = pd.read_pickle(constants.PREPROCESSED_FORECAST_DATA_FILE_PATH)
revenue2020     = pd.read_pickle(constants.PREPROCESSED_REVENUE2020_FILE_PATH)
revenue2020A    = pd.read_pickle(constants.PREPROCESSED_REVENUE2020A_FILE_PATH)
atlas2          = pd.read_pickle(constants.PREPROCESSED_ATLAS_2_FILE_PATH)


# %%
historical_data = atlas2.reset_index().set_index("Service Start").sort_index(ascending=True)

historical_data_invoice_amount = historical_data["Invoice Amount"]
historical_data_invoice_count = historical_data.groupby("Service Start").count()["Invoice Amount"]

# Critical
historical_data_invoice_amount_cumulative = historical_data["Invoice Amount"].cumsum()
historical_data_invoice_count_cumulative = historical_data.groupby("Service Start").count()["Invoice Amount"].cumsum()

# Extra
historical_data_invoice_mean = historical_data.groupby("Service Start").mean()["Invoice Amount"]
historical_data_nbr_users = historical_data["Number of Users"]
historical_data_nbr_customers = historical_data.groupby("Service Start").count()["Customers"]

historical_data_nbr_users_cumulative = historical_data["Number of Users"].cumsum()
historical_data_nbr_customers_cumulative = historical_data.groupby("Service Start").count()["Customers"].cumsum()


# %%
historical_data_invoice_amount_cumulative.diff()


# %%
mc = MCSimulation_Generic(
    value_list = historical_data_invoice_amount_cumulative,
    num_simulation=100,
    num_trailing_points = 10
)

mc.calc_cumulative_return()



# mc_data.columns.get_level_values(1).unique()


# %%
historical_data_invoice_amount_cumulative.hvplot.line()


# %%
historical_data_invoice_count_cumulative.hvplot.line()


# %%
historical_data_nbr_users_cumulative.hvplot.line()


# %%
historical_data_nbr_customers_cumulative.hvplot.line()


# %%



