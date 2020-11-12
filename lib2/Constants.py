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

class Constants:
    def __init__(self):

        # Directories
        self.LOOKUP_TABLES_DIR              = Path("../Resources/LookupTables")
        self.DATA_DIR_RAW                   = Path("../Resources/01_Raw")
        self.DATA_DIR_ANONYMIZED            = Path("../Resources/02_Anonymized")
        self.DATA_DIR_PREPROCESSED          = Path("../Resources/03_Preprocessed")
        self.DATA_DIR_PROCESSED             = Path("../Resources/04_Processed")

        # Lookup table files
        self.LUT_CUSTOMER_NAME_FILE_PATH    = os.path.join(self.LOOKUP_TABLES_DIR, Path("LUT_CustomerName.json"))

        # Raw data files
        self.RAW_ATLAS_FILE_PATH            = os.path.join(self.DATA_DIR_RAW, Path("ATLAS.csv"))
        self.RAW_FORECAST_DATA_FILE_PATH    = os.path.join(self.DATA_DIR_RAW, Path("2021 forecast CSV.csv"))
        self.RAW_REVENUE2020_FILE_PATH      = os.path.join(self.DATA_DIR_RAW, Path("Revenue2020.csv"))
        self.RAW_REVENUE2020A_FILE_PATH     = os.path.join(self.DATA_DIR_RAW, Path("Revenue2020A.csv"))
        self.RAW_ATLAS_2_FILE_PATH          = os.path.join(self.DATA_DIR_RAW, Path("ATLAS with Address.csv"))

        # Anonymized raw data files
        self.ANON_ATLAS_FILE_PATH           = os.path.join(self.DATA_DIR_ANONYMIZED, Path("ATLAS.csv"))
        self.ANON_FORECAST_DATA_FILE_PATH   = os.path.join(self.DATA_DIR_ANONYMIZED, Path("2021 forecast CSV.csv"))
        self.ANON_REVENUE2020_FILE_PATH     = os.path.join(self.DATA_DIR_ANONYMIZED, Path("Revenue2020.csv"))
        self.ANON_REVENUE2020A_FILE_PATH    = os.path.join(self.DATA_DIR_ANONYMIZED, Path("Revenue2020A.csv"))
        self.ANON_ATLAS_2_FILE_PATH         = os.path.join(self.DATA_DIR_ANONYMIZED, Path("ATLAS with Address.csv"))

        # Preprocessed data files
        self.PREPROCESSED_ATLAS_FILE_PATH           = os.path.join(self.DATA_DIR_PREPROCESSED, Path("ATLAS.pkl"))
        self.PREPROCESSED_FORECAST_DATA_FILE_PATH   = os.path.join(self.DATA_DIR_PREPROCESSED, Path("2021 forecast CSV.pkl"))
        self.PREPROCESSED_REVENUE2020_FILE_PATH     = os.path.join(self.DATA_DIR_PREPROCESSED, Path("Revenue2020.pkl"))
        self.PREPROCESSED_REVENUE2020A_FILE_PATH    = os.path.join(self.DATA_DIR_PREPROCESSED, Path("Revenue2020A.pkl"))
        self.PREPROCESSED_ATLAS_2_FILE_PATH         = os.path.join(self.DATA_DIR_PREPROCESSED, Path("ATLAS with Address.pkl"))

        # Preprocessed, combined data
        self.PREPROCESSED_COMBINED_DATA_FILE_PATH         = os.path.join(self.DATA_DIR_PREPROCESSED, Path("CombinedData.pkl"))

        # Processed data files
