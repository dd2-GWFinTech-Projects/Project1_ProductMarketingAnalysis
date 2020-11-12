# Import libraries and dependencies
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import hvplot.pandas
import panel as pn
from pathlib import Path
from dotenv import load_dotenv
from panel.interact import interact
from panel import widgets
from string import digits
import csv
import json
import numpy as np
import dateparser
import numpy as np
import pandas as pd
import os
import datetime as dt
import pytz
from Constants import Constants

class DateProcessingTools:

    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level

    def extract_year_month_quarter(self, date_list):
        """
        Extract to categorize data by Year, Month, and each Quarter.

        Parameters
        ----------
        date_list: list[pandas.Timestamp]
            List of dates to extract Year/Month/Quarter from.

        Returns
        -------
        list[list[int], list[int], list[int]]
            Three lists containing the year, month, and quarter integers.
        """
        
        year_column = []
        month_column = []
        quarter_column = []
        
        for date in date_list:
            year_column.append(date.year)
            month_column.append(date.month)
            quarter_column.append(date.quarter)
        
        return [year_column, month_column, quarter_column]
    
    def extract_and_append_year_month_quarter(self, data_frame, column_name):
        """
        Extract to categorize data by Year, Month, and each Quarter, and append as columns.

        Parameters
        ----------
        data_frame: pandas.DataFrame
            DataFrame to append columns to.
        column_name: string
            Name of the column from which Year/Month/Quarter is exracted.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with the Year/Month/Quarter columns appended.
        """
        columns = self.extract_year_month_quarter(data_frame[column_name])
        periods_df = pd.DataFrame({"Year":columns[0],"Monthly": columns[1], "Quarterly": columns[2]})
        return pd.concat([data_frame.reset_index(), periods_df], axis='columns', join="inner")

