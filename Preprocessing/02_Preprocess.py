# # Initial imports
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import hvplot.pandas
# import panel as pn
# from pathlib import Path
# # from dotenv import load_dotenv22
# from panel.interact import interact
# from panel import widgets
# from string import digits
# import csv
# import json
# import numpy as np
# import dateparser

# pn.extension()

# # %matplotlib inline

# debug_level = 3

# # Function definitions: TODO move to .py

# ## Data cleaning
# def remove_strings_from_customer_names(original_customer_name):
#     invalid_strings = ["PYMT", "DUE"]
#     for invalid_item in invalid_strings:
#         original_customer_name = original_customer_name.replace(invalid_item, "")
#     return original_customer_name.strip()

# def remove_numbers_from_customer_names(original_customer_name):
#     remove_digits = str.maketrans('', '', digits) 
#     return original_customer_name.translate(remove_digits).strip()  

# def cleanup_customer_names(paying_customers_raw):
#     paying_customers_cleanedup = []
#     for customer in paying_customers_raw:
#         corrected_customer_name = str(customer)
#         #corrected_customer_name = str(customer).upper()
#         corrected_customer_name = remove_strings_from_customer_names(corrected_customer_name)
#         corrected_customer_name = remove_numbers_from_customer_names(corrected_customer_name)
#         #corrected_customer_name = corrected_customer_name.title()
#         paying_customers_cleanedup.append(corrected_customer_name)
#     return paying_customers_cleanedup

# def build_name_mapping(paying_customers_cleanedup):
#     name_mapping = {}
#     n = 1
#     for customer in paying_customers_cleanedup:
#         if not customer in name_mapping:
#             name_mapping[customer] = "University " + str(n)
#             n += 1
#     return name_mapping

# def read_name_mapping():
#     with open(MAPPING_FILE_PATH, "r") as file:
#         return json.loads(file.read())

# def anonymize_customer_list(customer_list):
#     anonymized_customer_list = []
#     for customer in customer_list:
#         anonymized_customer_list.append(customer_name_mapping[customer])
#     return anonymized_customer_list

# # Constants - TODO Move to .py
# MAPPING_DIR                     = Path("../Resources/Mappings")
# DATA_DIR_RAW                    = Path("../Resources/01_Raw")
# DATA_DIR_ANONYMIZED             = Path("../Resources/02_Anonymized")
# DATA_DIR_PREPROCESSED           = Path("../Resources/03_Preprocessed")
# DATA_DIR_PROCESSED              = Path("../Resources/04_Processed")

# MAPPING_FILE_PATH               = os.path.join(MAPPING_DIR, Path("CustomerNameMapping.json"))

# RAW_ATLAS_FILE_PATH             = os.path.join(DATA_DIR_RAW, Path("ATLAS.csv"))
# RAW_FORECAST_DATA_FILE_PATH     = os.path.join(DATA_DIR_RAW, Path("2021 forecast CSV.csv"))
# RAW_REVENUE2020_FILE_PATH       = os.path.join(DATA_DIR_RAW, Path("Revenue2020.csv"))
# RAW_REVENUE2020A_FILE_PATH      = os.path.join(DATA_DIR_RAW, Path("Revenue2020A.csv"))

# ANON_ATLAS_FILE_PATH            = os.path.join(DATA_DIR_ANONYMIZED, Path("ATLAS.csv"))
# ANON_FORECAST_DATA_FILE_PATH    = os.path.join(DATA_DIR_ANONYMIZED, Path("2021 forecast CSV.csv"))
# ANON_REVENUE2020_FILE_PATH      = os.path.join(DATA_DIR_ANONYMIZED, Path("Revenue2020.csv"))
# ANON_REVENUE2020A_FILE_PATH     = os.path.join(DATA_DIR_ANONYMIZED, Path("Revenue2020A.csv"))

# def cleanup_date_string_list(date_string_list):
#     date_list = []
#     for date_string in date_string_list:
#         try:
#             date_list.append(parse_date_string(date_string))
#         except:
#             print(f"Failed to parse: {date_string}")
#     return date_list

# def cleanup_dollar_string(dollars_string):
#     return float(dollars_string.replace('$','').replace(',', ''))

# def cleanup_dollar_string_list(dollars_list_in):
#     dollars_list_out = []
#     for dollars_string in dollars_list_in:
#         # debug_level >= 3 and print(f"Parsing: {dollars_string}")
#         try:
#             dollars_list_out.append( cleanup_dollar_string(dollars_string) )
#         except:
#             debug_level >= 2 and print(f"Failed to parse: {dollars_string}")
#     return dollars_list_out


# def extract_subscription_dates_list(subscription_dates_string_list):
#     """
#     Parses a subscription date string from the ATLAS data export.

#     A sample is: "1 Year Subscription 3/18/15 to 6/30/16"

#     Parameters
#     ----------
#     subscription_dates_string_list: list[string]
#         List or iterable of strings in the ATLAS subscription date string format.
    
#     Returns
#     -------
#     [list, list]
#         List containing one list of start dates, followed by one list of end dates.
#     """

#     subscription_dates_start_list = []
#     subscription_dates_end_list = []

#     for subscription_dates_string in subscription_dates_string_list:

#         debug_level >= 2 and print(f"extract_subscription_dates_list - parsing: {subscription_dates_string}")

#         # Find "Subscription"
#         split1 = subscription_dates_string.find("Subscription")
#         split2 = split1 + len("Subscription")
#         if split1 < 0:
#             # Failed so look for "Subscr"
#             split1 = subscription_dates_string.find("Subscr")
#             split2 = split1 + len("Subscr")

#         # Split
#         subscription_str = subscription_dates_string[0:split2].strip()
#         date_range = subscription_dates_string[split2:].strip()

#         # Find "to"
#         split1 = date_range.find("to")
#         split2 = split1 + len("to")
#         if split1 < 0:
#             # Failed so find "-"
#             split1 = date_range.find("-")
#             split2 = split1 + len("-")
        
#         # Look for bad data after the date
#         split3 = date_range.find("2nd inv")

#         if split3 < 0:
#             split3 = date_range.find("additional users")

#         # No bad data found after date
#         if split3 < 0:
#             split3 = len(date_range)
        
#         # Split
#         date1_str = date_range[0:split1].strip()
#         date2_str = date_range[split2:split3].strip()

#         # Parse dates
#         debug_level >= 2 and print(f"date1_str: {date1_str}  date2_str: {date2_str}")
#         date1 = parse_date_string(date1_str)
#         date2 = parse_date_string(date2_str)
#         debug_level >= 2 and print(f"    date1_str: {date1_str}  date1: {date1}")
#         debug_level >= 2 and print(f"    date2_str: {date2_str}  date2: {date2}")

#         # Build lists
#         subscription_dates_start_list.append(date1)
#         subscription_dates_end_list.append(date2)
    
#     return [ subscription_dates_start_list, subscription_dates_end_list ]

# def parse_date_string(date_str):
    
#     debug_level >= 3 and print(f"parse_date_string - date_str before: {date_str}")

#     # Basic cleanup
#     date_str = date_str.replace("//", "/")
#     date_str = date_str.strip("/")
    
#     debug_level >= 3 and print(f"parse_date_string - date_str after: {date_str}")

#     # Parsing
#     try:
#         date = dateparser.parse(date_str)
#         return convert_datetime_to_timestamp(date)
#     except:
#         print(f"Failed to parse: {date_str}")
#         return ""

# def convert_datetime_to_timestamp(date_datetime):
#     try:
#         return pd.Timestamp(date_datetime.isoformat(), tz="America/New_York", tzinfo=date_datetime.tzinfo)
#     except:
#         return None

# # Read anonymized data
# atlas           = pd.read_csv(ANON_ATLAS_FILE_PATH, index_col="Customers")
# forecast        = pd.read_csv(ANON_FORECAST_DATA_FILE_PATH, index_col="Organization Name")
# revenue2020     = pd.read_csv(ANON_REVENUE2020_FILE_PATH, index_col="Name")
# revenue2020A    = pd.read_csv(ANON_REVENUE2020A_FILE_PATH, index_col="Payee Name")

# # dates_of_service = extract_subscription_dates_list(atlas["Dates of service "])
# # dates_of_service

# s = [
#     "1 Year 6 Months Subscr 05/01/2016 to 12/17/17",
#     "3 Years Subscription 9/29/19 to 9/29/22 2nd inv to reflect adjustment",
#     "3 Years Subscription 5/22/19 to 5/31/22 additional users adj",
#     "3 Years Subscription 5/22/19 to 5/31/22 additional users",
#     "1 Year renewal",
#     "1 Year Subscription 3/1/1/ to 2/28/19"
# ]
# s2 = extract_subscription_dates_list(s)
# s2

# # s2 = [[1, 2, 3, None]]
# # df = pd.DataFrame(s2[0])
# # # df.dropna(inplace=True)
# # df.size
# # df

# # Clean up ATLAS data

# ## Invoice Date
# atlas["Invoice Date"]       = cleanup_date_string_list(atlas["Invoice Date"])

# ## Invoice Amount
# # atlas["Invoice Amount"]
# # out = cleanup_dollar_string_list(atlas["Invoice Amount"])
# # out
# atlas["Invoice Amount"]      = cleanup_dollar_string_list(atlas["Invoice Amount"])
# # atlas["Invoice Amount"]     = cleanup_dollar_string_list(atlas["Invoice Amount"])

# ## Dates of service
# dates_of_service = extract_subscription_dates_list(atlas.iloc[0:20]["Dates of service "])
# # dates_of_service
# # atlas["Service Start"]      = dates_of_service[0]
# # atlas["Service End"]        = dates_of_service[1]
# # atlas.drop(columns=["Dates of service"], inplace=True)

# atlas.head()
