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
from pytimeparse import parse


# Local imports
from Constants import Constants


class CustomerNameCleaningFunctions:
    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level

    def remove_strings_from_customer_names(self, original_customer_name):
        invalid_strings = ["PYMT", "DUE"]
        for invalid_item in invalid_strings:
            original_customer_name = original_customer_name.replace(invalid_item, "")
        return original_customer_name.strip()

    def remove_numbers_from_customer_names(self, original_customer_name):
        remove_digits = str.maketrans('', '', digits) 
        return original_customer_name.translate(remove_digits).strip()  

    def cleanup_customer_names(self, paying_customers_raw):
        paying_customers_cleanedup = []
        for customer in paying_customers_raw:
            corrected_customer_name = str(customer)
            #corrected_customer_name = str(customer).upper()
            corrected_customer_name = self.remove_strings_from_customer_names(corrected_customer_name)
            corrected_customer_name = self.remove_numbers_from_customer_names(corrected_customer_name)
            #corrected_customer_name = corrected_customer_name.title()
            paying_customers_cleanedup.append(corrected_customer_name)
        return paying_customers_cleanedup

    def anonymize_customer_list(self, customer_list, customer_name_mapping):
        anonymized_customer_list = []
        for customer in customer_list:
            anonymized_customer_list.append(customer_name_mapping[customer])
        return anonymized_customer_list

    def set_customers_index(self, df, customer_list_anonymized, customer_column_name):
        df.reset_index(inplace=True)
        df[customer_column_name] = customer_list_anonymized
        df.set_index(customer_column_name, inplace=True)
        return df


class DateCleaningFunctions:
    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level
        
    def cleanup_date_string_list(self, date_string_list):
        date_list = []
        for date_string in date_string_list:
            try:
                date_list.append(self.parse_date_string(date_string))
            except:
                self.debug_level >= 2 and print(f"Failed to parse: {date_string}")
                date_list.append(None)
        return date_list

    def cleanup_dollar_string(self, dollars_string):
        return float(dollars_string.replace('$','').replace(',', ''))

    def cleanup_dollar_string_list(self, dollars_list_in):
        dollars_list_out = []
        for dollars_string in dollars_list_in:
            # debug_level >= 3 and print(f"Parsing: {dollars_string}")
            try:
                dollars_list_out.append( self.cleanup_dollar_string(dollars_string) )
            except:
                self.debug_level >= 2 and print(f"Failed to parse: {dollars_string}")
                dollars_list_out.append(None)
        return dollars_list_out

    def parse_date_string(self, date_str):
        
        self.debug_level >= 3 and print(f"parse_date_string - date_str before: {date_str}")

        # Basic cleanup
        date_str = date_str.replace("//", "/")
        date_str = date_str.strip("/")
        
        self.debug_level >= 3 and print(f"parse_date_string - date_str after: {date_str}")

        # Parsing
        try:
            date = dateparser.parse(date_str)
            return self.convert_datetime_to_timestamp(date)
        except:
            self.debug_level >= 3 and print(f"Failed to parse: {date_str}")
            return None

    def convert_datetime_to_timestamp(self, date_datetime):
        try:
            return pd.Timestamp(date_datetime.isoformat(), tz="America/New_York", tzinfo=date_datetime.tzinfo)
        except:
            return None


class DurationParsing:
    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level
        self.duration_lookup_table = {
            "30 DAY":       pd.Timedelta(30, unit="days"),
            "3 MONTH":      pd.Timedelta(30 * 3, unit="days"),
            "5 MONTH":      pd.Timedelta(30 * 5, unit="days"),
            "6 MONTH":      pd.Timedelta(30 * 6, unit="days"),
            "1 YEAR":       pd.Timedelta(365 * 1, unit="days"),
            "ANNUAL":       pd.Timedelta(365 * 1, unit="days"),
            "18 MO":        pd.Timedelta(30 * 18, unit="days"),
            "18 MONTH":     pd.Timedelta(30 * 18, unit="days"),
            "2 YEAR":       pd.Timedelta(365 * 2, unit="days"),
            "3 YEAR":       pd.Timedelta(365 * 3, unit="days")
            }

    def parse_duration_str_list(self, duration_str_list):
        return [(lambda x: self.parse_duration_str(x))(duration_str) for duration_str in duration_str_list]

    def parse_duration_str(self, duration_str):
        
        # Normalize input string
        duration_str = str(duration_str).upper().strip().strip("S").replace("-", " ")
        
        try:
            # Try lookup table
            if duration_str in self.duration_lookup_table:
                return self.duration_lookup_table[duration_str]
        except:
            self.debug_level >= 3 and print(f"parse_duration_str: Failed to parse {duration_str} using lookup table.")

        try:
            # Try Pandas Timedelta parser
            return pd.to_timedelta(duration_str)
        except:
            self.debug_level >= 3 and print(f"parse_duration_str: Failed to parse {duration_str} using Pandas Timedelta parser.")

        try:
            # Try pytimeparse parser
            num_seconds = parse(duration_str)
            return pd.Timedelta(num_seconds, unit="seconds")
        except:
            self.debug_level >= 3 and print(f"parse_duration_str: Failed to parse {duration_str} using pytimeparse parser.")
        
        return None


class SpecializedDateCleaningFunctions:

    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level
        self.tool_date = DateCleaningFunctions(debug_level)
    
    def extract_subscription_dates_list(self, subscription_dates_string_list):
        """
        Parses a subscription date string from the ATLAS data export.

        A sample is: "1 Year Subscription 3/18/15 to 6/30/16"

        Parameters
        ----------
        subscription_dates_string_list: list[string]
            List or iterable of strings in the ATLAS subscription date string format.
        
        Returns
        -------
        [list, list]
            List containing one list of start dates, followed by one list of end dates.
        """

        subscription_dates_start_list = []
        subscription_dates_end_list = []

        for subscription_dates_string in subscription_dates_string_list:
            
            subscription_dates_string = str(subscription_dates_string)

            self.debug_level >= 2 and print(f"extract_subscription_dates_list - parsing: {subscription_dates_string}")

            # Find "Subscription"
            split1 = subscription_dates_string.find("Subscription")
            split2 = split1 + len("Subscription")
            if split1 < 0:
                # Failed so look for "Subscripture"
                split1 = subscription_dates_string.find("Subscripture")
                split2 = split1 + len("Subscripture")
            if split1 < 0:
                # Failed so look for "Subscr"
                split1 = subscription_dates_string.find("Subscr")
                split2 = split1 + len("Subscr")
            
            # Split
            subscription_str = subscription_dates_string[0:split2].strip()
            date_range = subscription_dates_string[split2:].strip()

            # Find "to"
            split1 = date_range.find("to")
            split2 = split1 + len("to")
            if split1 < 0:
                # Failed so find "-"
                split1 = date_range.find("-")
                split2 = split1 + len("-")
            
            # Look for bad data after the date
            split3 = date_range.find("2nd inv")

            if split3 < 0:
                split3 = date_range.find("additional users")

            # No bad data found after date
            if split3 < 0:
                split3 = len(date_range)
            
            # Split
            date1_str = date_range[0:split1].strip()
            date2_str = date_range[split2:split3].strip()

            # Parse dates
            self.debug_level >= 2 and print(f"date1_str: {date1_str}  date2_str: {date2_str}")
            date1 = self.tool_date.parse_date_string(date1_str)
            date2 = self.tool_date.parse_date_string(date2_str)
            self.debug_level >= 2 and print(f"    date1_str: {date1_str}  date1: {date1}")
            self.debug_level >= 2 and print(f"    date2_str: {date2_str}  date2: {date2}")

            # Build lists
            subscription_dates_start_list.append(date1)
            subscription_dates_end_list.append(date2)
        
        return [ subscription_dates_start_list, subscription_dates_end_list ]


class MappingFunctions:

    def __init__(self, debug_level):
        self.constants = Constants()
        self.debug_level = debug_level

    def build_name_mapping(self, paying_customers_cleanedup):
        name_mapping = {}
        n = 1
        for customer in paying_customers_cleanedup:
            if not customer in name_mapping:
                name_mapping[customer] = "University " + str(n)
                n += 1
        return name_mapping

    def write_customer_name_mapping(self, customer_name_mapping):
        with open(self.constants.LUT_CUSTOMER_NAME_FILE_PATH, "w") as file:
            file.write(json.dumps(customer_name_mapping))
    
    def read_customer_name_mapping(self):
        with open(self.constants.LUT_CUSTOMER_NAME_FILE_PATH, "r") as file:
            return json.loads(file.read())

    def write_lookup_table(self, lookup_table, file_path):
        with open(file_path, "w") as file:
            file.write(json.dumps(lookup_table))

    def read_lookup_table(self, file_path):
        with open(file_path, "r") as file:
            return json.loads(file.read())
