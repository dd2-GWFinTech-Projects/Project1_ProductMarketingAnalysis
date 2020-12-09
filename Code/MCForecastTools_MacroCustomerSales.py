# Import libraries and dependencies
import numpy as np
import pandas as pd
import os
import datetime as dt
import pytz

from UpgradeSequenceDataStructures import UpgradeType
from UpgradeSequenceDataStructures import CustomerBehaviorObservations
from UpgradeSequenceDataStructures import CustomerBehaviorClassifications

from TimeSeriesModels import TimeSeriesModelUtilities

from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerBehaviorNumbers


# ------------------------------------------------------------------------------
# Historical analysis tools
# ------------------------------------------------------------------------------


class MacroCustomerSales_HistoricalAnalysis:


    def __init__(self, debug_level=0):
        self.debug_level = debug_level


    def compute_rolling_std(self, macro_customer_behavior_values_nominal_list, window):
        return macro_customer_behavior_values_nominal_list.rolling(window).std()


# ------------------------------------------------------------------------------
# Simulation tools
# ------------------------------------------------------------------------------


#         # TODO Use conversion rates from each behavior classification to each other behavior classification




# class MacroCustomerSales_ForwardPredictor:

#     def __init__(self, debug_level=0):
#         self.debug_level = debug_level

#     def simulate_next_annual_numbers(self, macro_customer_behavior_counts_list):

#         conversion_rates = []
#         for macro_customer_behavior_counts in macro_customer_behavior_counts_list:
#             conversion_rates = []  # Compute running-average of year-to-year retention and/or conversion rates (totalcount -> new, new -> cont, new -> dropped, cont -> dropped, cont -> cont x3).

#         # For now, simply carry the last year's numbers into the next.
#         return macro_customer_behavior_counts_list[-1]


# class MacroCustomerSales_PredictionFuzzer:

#     def __init__(self, debug_level=0):
#         self.debug_level = debug_level

#     def predict_using_distribution(self, macro_customer_behavior_counts_nominal, macro_customer_behavior_counts_std):
#         mean_values = [
#             macro_customer_behavior_counts_nominal.nbr_new_customers,
#             macro_customer_behavior_counts_nominal.nbr_continued_loyal_customers,
#             macro_customer_behavior_counts_nominal.nbr_continued_at_risk_customers,
#             macro_customer_behavior_counts_nominal.nbr_continued_nominal_customers,
#             macro_customer_behavior_counts_nominal.nbr_dropped_customers
#         ]
#         std_values = [
#             macro_customer_behavior_counts_std.nbr_new_customers,
#             macro_customer_behavior_counts_std.nbr_continued_loyal_customers,
#             macro_customer_behavior_counts_std.nbr_continued_at_risk_customers,
#             macro_customer_behavior_counts_std.nbr_continued_nominal_customers,
#             macro_customer_behavior_counts_std.nbr_dropped_customers
#         ]
#         randomized_values = np.random.normal(mean_values, std_values)
#         return MacroCustomerBehaviorCounts(
#             randomized_values[0],
#             randomized_values[1],
#             randomized_values[2],
#             randomized_values[3],
#             randomized_values[4],
#         )


    def compute_annual_sales(self, macro_customer_behavior_counts, macro_customer_average_annual_sales):
        macro_customer_behavior_counts.nbr_new_customers * macro_customer_average_annual_sales.avg_annual_sales_new_customers






# ------------------------------------------------------------------------------
# Simulation framework
# ------------------------------------------------------------------------------


class ForwardPredictor:
    def __init__(self, debug_level,
            all_x_values, series_key_list,
            values_dict,
            model_type, opts_dict):

        self.debug_level = debug_level
        self.all_x_values = all_x_values
        self.series_key_list = series_key_list
        self.values_dict = values_dict
        self.model_type = model_type
        self.opts_dict = opts_dict

        self.num_x_values = len(all_x_values)
        self.time_series_model_utilities = TimeSeriesModelUtilities()
        self.reset()
    
    def reset(self):
        self.i = 0

    def has_next(self):
        return self.i < self.num_x_values

    # Predict one forward iteration and return the value foreach series, inside a dictionary of single-item-lists
    def predict_next(self):

        # Slice x data for the time series model
        historical_x_values = self.all_x_values[ 0 : self.i ]
        prediction_x_values = self.all_x_values[ self.i : self.num_x_values ]

        prediction_map = self.time_series_model_utilities.init_series_map(self.series_key_list)
        for series_key in self.series_key_list:

            # Slice y data for the time series model
            historical_y_values = self.time_series_model_utilities.split_series_map(self.values_dict, self.i)

            # Build predictor
            model = self.time_series_model_utilities.build_model(
                self.model_type, 
                historical_x_values,
                self.series_key_list,
                historical_y_values, historical_y_values,
                self.opts_dict)

            # Train
            model.train()

            # Predict
            prediction_y_values = model.predict(prediction_x_values)

            # Store in the series map
            prediction_map[series_key] = prediction_y_values
        
        # Advance index
        self.i += 1

        return prediction_map


class Fuzzer:

    def __init__(self, debug_level):
        self.debug_level = debug_level
    
    def fuzz(self, series_map, std_series_map):

        series_key_list = list(series_map.keys())
        for series_key in series_key_list:
            
            last_value = series_map[series_key][-1]
            std_value = std_series_map[series_key][-1]

            # Generate fuzzed value
            fuzzed_value = np.random.normal(last_value, std_value)

            # Update last value with fuzzed value
            series_map[series_key][-1] = fuzzed_value

        return series_map


class MacroCustomerSales_MCSimulation:

    def __init__(self,
                debug_level, series_key_list,
                forward_value_predictor,
                forward_std_predictor,
                prediction_fuzzer,
                num_simulation,
                simulation_value_title,
                num_prediction_time_steps):

        self.debug_level = debug_level
        self.series_key_list = series_key_list
        self.forward_value_predictor = forward_value_predictor
        self.forward_std_predictor = forward_std_predictor
        self.prediction_fuzzer = prediction_fuzzer
        self.num_simulation = num_simulation
        self.simulation_value_title = simulation_value_title
        self.num_prediction_time_steps = num_prediction_time_steps

        self.time_series_model_utilities = TimeSeriesModelUtilities()
        self.simulation_values = None

    # --------------------------------------------------------------------------
    # Simulation
    # --------------------------------------------------------------------------

    def run(self):

        # Initialize output structure
        self.simulation_values = []

        # Iterate over simulations
        for n in self.num_simulation:

            if n % 10 == 0:
                print(f"Running Monte Carlo simulation number {n}.")

            # Initialize empty simulation run map
            run_series_map = self.time_series_model_utilities.init_series_map(self.series_key_list)

            # Iterate through time series, building one future prediction at a time
            while self.forward_value_predictor.has_next():
                
                # Predict the next time step
                predicted_y_values = self.forward_value_predictor.predict_next()
                predicted_std_values = self.forward_std_predictor.predict_next()

                # Append time step
                run_series_map = self.time_series_model_utilities.join_series_maps(run_series_map, predicted_y_values)
                std_series_map = self.time_series_model_utilities.join_series_maps(std_series_map, predicted_std_values)

                # Fuzz the prediction (apply randomness)
                run_series_map = self.prediction_fuzzer.fuzz(run_series_map, std_series_map)

            # Append simulation run results
            self.simulation_values.append(run_series_map)

        return self.simulation_values

    # --------------------------------------------------------------------------
    # Post-Processing
    # --------------------------------------------------------------------------

    def extract_last_values(self):

        # Extract last values from each run and collect into a last values series map
        self.last_values_map = self.time_series_model_utilities.init_series_map(self.series_key_list)
        last_item_split_index = len(self.simulation_values[0][self.series_key_list]) - 1

        for run_series_map in self.simulation_values:
            run_first_values, run_last_values = self.time_series_model_utilities.split_series_map(run_series_map, last_item_split_index)
            self.last_values_map = self.time_series_model_utilities.join_series_maps(self.last_values_map, run_last_values)
        
        return self.last_values_map
    
    def compute_statistics(self):

        # Calculate 95% confidence intervals for final estimated values
        self.confidence_intervals = self.time_series_model_utilities.init_series_map(self.series_key_list)
        for series_key in self.series_key_list:
            series_last_values = self.last_values_map[series_key]
            self.confidence_intervals[series_key] = np.quantile(np.array(series_last_values), q=[0.025, 0.975])

        return self.confidence_intervals


        # TODO Upgrade to compute predicted sales numbers for the selected ind vars;
        #   def compute_sales_atinstantintime(nbr_loyal_customers, nbr_new_customers, nbr_renew_customers, nbr_dropouts)
        #   def compute_sales_atinstantintime(nbr_customers_size_parameter, loyal_customers_rate, new_customers_rate, renew_customers_rate, dropouts_rate)

        # TODO Switch to enable best-case and worst-case instead of normal distr

    # --------------------------------------------------------------------------
    # Plotting & Report Generation
    # --------------------------------------------------------------------------

    def plot_simulation(self, figsize=(20, 8)):

        # Build dataframe for plotting
        series_simulation_df_map = self.extract_simulation_values_to_df(self.simulation_values)

        # Use Pandas plot function to plot the return data
        plot_title = f"{self.num_simulation} Simulations of {self.simulation_value_title} Trajectories Over the Next {self.num_prediction_time_steps} Time Steps"

        self.simulation_plt = None
        for series_key in self.series_key_list:
            series_simulation_df = series_simulation_df_map[series_key]
            if (self.simulation_plt is None):
                self.simulation_plt = series_simulation_df.plot(kind="line", legend=False, title=plot_title)
            else:
                self.simulation_plt.plot(series_simulation_df, kind="line")

        return self.simulation_plt

    def plot_distribution(self, width=800, height=500):

        # Use the plot function to create a probability distribution histogram of simulated ending values
        # with markings for a 95% confidence interval

        self.plt_map = {}
        
        last_values_df = self.time_series_model_utilities.convert_series_map_to_df(self.last_values_map)

        for series_key in self.series_key_list:

            last_values_series = last_values_df[series_key]

            # Generate plot
            plot_title = f"Distribution of Final {self.simulation_value_title} Across All {self.num_simulation} Simulations - {str(series_key)} Series"
            plt = last_values_series.plot(kind='hist', density=True, title=plot_title, width=width, height=height)
            plt.axvline(self.confidence_intervals[series_key].iloc[0], color='r')
            plt.axvline(self.confidence_intervals[series_key].iloc[1], color='r')

            # Append to output structure
            self.plt_map[series_key] = plt
        
        return self.plt_map
    
    def summarize_cumulative_return(self):

        self.metrics_map = {}
        last_values_df = self.time_series_model_utilities.convert_series_map_to_df(self.last_values_map)

        for series_key in self.series_key_list:

            last_values_series = last_values_df[series_key]

            metrics = last_values_series.describe()

            ci_series = self.confidence_intervals[series_key]
            ci_series.index = ["95% CI Lower", "95% CI Upper"]
    
            metrics.append(ci_series)

            self.metrics_map[series_key] = metrics

        return self.metrics_map

    # --------------------------------------------------------------------------
    # Utility Functions
    # --------------------------------------------------------------------------

    def extract_simulation_values_to_df(self, simulation_values):
        
        # Populate each series with simulated runs
        series_simulation_df_map = {}
        for series_key in self.series_key_list:
            
            # Initialize empty DataFrame
            series_simulation_df_map[series_key] = pd.DataFrame(index = self.forward_value_predictor.all_x_values)

            # Populate with simulated runs
            for run_index in self.num_simulation:
                series_simulation_df_map[series_key][run_index] = simulation_values[run_index][series_key]

        return series_simulation_df_map
