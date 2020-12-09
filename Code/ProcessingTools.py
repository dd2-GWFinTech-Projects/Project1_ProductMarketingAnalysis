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
import calendar
from Constants import Constants
import math

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
    
    def parse_month_number_list(self, month_number_list):
        month_name_list = []
        # [(lambda x: self.parse_month_number)(x) for x in columns[1]],
        for month_number in month_number_list:
            month_name = self.parse_month_number(month_number)
            month_name_list.append(month_name)
        return month_name_list

    def parse_month_number(self, month_number):
        # print(f"Month number {month_number}")
        if not math.isnan(month_number):
            return calendar.month_name[int(month_number)]
        else:
            return ""
    
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
        periods_df = pd.DataFrame({
            column_name + "_Year": columns[0],
            column_name + "_Month": columns[1],
            column_name + "_MonthName": self.parse_month_number_list(columns[1]),
            column_name + "_Quarter": columns[2] })
        return pd.concat([data_frame.reset_index(), periods_df], axis='columns', join="inner").set_index(data_frame.index.name)

        # columns = self.extract_year_month_quarter(data_frame[column_name])
        # periods_df = pd.DataFrame({ column_name + "_Year":columns[0], column_name + "_Month": columns[1], column_name + "_Quarter": columns[2]})
        # return pd.concat([data_frame.reset_index(), periods_df], axis='columns', join="inner")
