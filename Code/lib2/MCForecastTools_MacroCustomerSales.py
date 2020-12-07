# Import libraries and dependencies
import numpy as np
import pandas as pd
import os
import datetime as dt
import pytz
from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerBehaviorCounts
from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerAverageAnnualSales
from UpgradeSequenceDataStructures import UpgradeType
from UpgradeSequenceDataStructures import CustomerBehaviorObservations
from UpgradeSequenceDataStructures import CustomerBehaviorClassifications


# ------------------------------------------------------------------------------
# Historical analysis tools
# ------------------------------------------------------------------------------


class MacroCustomerSales_HistoricalAnalysis:
    
    def __init__(self, debug_level=0):
        self.debug_level = debug_level
    
    def compute_rolling_std(self, macro_customer_behavior_values_nominal_list, window):

        new_customers_value_list = macro_customer_behavior_values_nominal_list[CustomerBehaviorClassifications.New]
        continued_loyal_customers_value_list = macro_customer_behavior_values_nominal_list[CustomerBehaviorClassifications.Continued_Loyal]
        continued_at_risk_customers_value_list = macro_customer_behavior_values_nominal_list[CustomerBehaviorClassifications.Continued_AtRisk]
        continued_nominal_customers_value_list = macro_customer_behavior_values_nominal_list[CustomerBehaviorClassifications.Continued_Nominal]
        dropped_customers_value_list = macro_customer_behavior_values_nominal_list[CustomerBehaviorClassifications.Dropped]
        year_list = macro_customer_behavior_values_nominal_list["year"]

        # df = pd.DataFrame({'A': [0, 100, 110, 115, 120], 'B': [0, 100, 110, 115, 120]}).T
        # df.rolling(window=3, axis=1).std()

        df = pd.DataFrame(macro_customer_behavior_values_nominal_list).T
        return df.rolling(window, axis=1)



        # msft_df.rolling(window=7).std().plot()
        new_customers_value_list_std = new_customers_value_list.rolling(window).std()




        macro_customer_behavior_values_std_list = 
        return macro_customer_behavior_values_std_list


# ------------------------------------------------------------------------------
# Simulation tools
# ------------------------------------------------------------------------------

class MacroCustomerSales_ForwardPredictor:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def simulate_next_annual_numbers(self, macro_customer_behavior_counts_list):

        # TODO Use average sales per year for each customer???
        # TODO Use conversion rates from each behavior classification to each other behavior classification
        # TODO Trend-based prediction. Time series regression?

        conversion_rates = []
        for macro_customer_behavior_counts in macro_customer_behavior_counts_list:
            conversion_rates = []  # Compute running-average of year-to-year retention and/or conversion rates (totalcount -> new, new -> cont, new -> dropped, cont -> dropped, cont -> cont x3).

        # For now, simply carry the last year's numbers into the next.
        return macro_customer_behavior_counts_list[-1]


class MacroCustomerSales_InstantaneousVariation:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def predict_using_distribution(self, macro_customer_behavior_counts_nominal, macro_customer_behavior_counts_std):
        mean_values = [
            macro_customer_behavior_counts_nominal.nbr_new_customers,
            macro_customer_behavior_counts_nominal.nbr_continued_loyal_customers,
            macro_customer_behavior_counts_nominal.nbr_continued_at_risk_customers,
            macro_customer_behavior_counts_nominal.nbr_continued_nominal_customers,
            macro_customer_behavior_counts_nominal.nbr_dropped_customers
        ]
        std_values = [
            macro_customer_behavior_counts_std.nbr_new_customers,
            macro_customer_behavior_counts_std.nbr_continued_loyal_customers,
            macro_customer_behavior_counts_std.nbr_continued_at_risk_customers,
            macro_customer_behavior_counts_std.nbr_continued_nominal_customers,
            macro_customer_behavior_counts_std.nbr_dropped_customers
        ]
        randomized_values = np.random.normal(mean_values, std_values)
        return MacroCustomerBehaviorCounts(
            randomized_values[0],
            randomized_values[1],
            randomized_values[2],
            randomized_values[3],
            randomized_values[4],
        )


    def compute_annual_sales(self, macro_customer_behavior_counts, macro_customer_average_annual_sales):
        macro_customer_behavior_counts.nbr_new_customers * macro_customer_average_annual_sales.avg_annual_sales_new_customers






# ------------------------------------------------------------------------------
# Simulation framework
# ------------------------------------------------------------------------------

class MacroCustomerSales_MCSimulation:
    def __init__(self,
        value_title,
        value_list,
        num_simulation=1000, num_trailing_points=50,
        scale_results=True,
        allow_negative_returns=True,
        debug_level=0
        ):
        self.value_title = value_title
        self.value_list = value_list
        self.nSim = num_simulation
        self.num_trailing_points = num_trailing_points
        self.simulated_return = ""

        # Grab initial value to use for scaling the results.
        if scale_results:
            self.initial_value = value_list[0]
        else:
            self.initial_value = 1.0
        
        self.allow_negative_returns = allow_negative_returns


        
    def calc_cumulative_return(self):
        """
        Calculates the cumulative return of a stock over time using a Monte Carlo simulation (Brownian motion with drift).

        """

        # Get closing prices of each stock
        value_list = self.value_list  # last_prices
        
        # Calculate the mean and standard deviation of daily returns for each stock
        value_list_change = value_list.pct_change().dropna() # daily_returns

        mean_change = value_list_change.mean()  # mean_returns
        std_change = value_list_change.std()  # std_returns

        # Initialize empty Dataframe to hold simulated prices
        portfolio_cumulative_returns = None
        
        # Run the simulation of projecting stock prices 'nSim' number of times
        for n in range(self.nSim):
        
            if n % 10 == 0:
                print(f"Running Monte Carlo simulation number {n}.")
        
            # Create a list of lists to contain the simulated values for each stock
            simvals = value_list.to_list()

            # TODO Ensure x axis is ordered.
            # TODO Ensure x axis is evenly spaced.

            # Simulate the returns for each trading day
            for i in range(self.num_trailing_points):
    
                # Calculate the simulated price using the last price within the list

                # print(f"simvals type {type(simvals)}")

                # TODO Upgrade to handle multiple ind variables

                # TODO Upgrade to compute predicted sales numbers for the selected ind vars;
                #   def compute_sales_atinstantintime(nbr_loyal_customers, nbr_new_customers, nbr_renew_customers, nbr_dropouts)
                #   def compute_sales_atinstantintime(nbr_customers_size_parameter, loyal_customers_rate, new_customers_rate, renew_customers_rate, dropouts_rate)

                # TODO Switch to enable best-case and worst-case instead of normal distr
                d = np.random.normal(mean_change, std_change)
                if not self.allow_negative_returns:
                    d = np.abs(d)
                simvals.append(simvals[-1] * (1 + d))

    
            # Calculate the daily returns of simulated prices
            sim_df = pd.DataFrame(simvals).pct_change()
    
            # Calculate the normalized, cumulative return series
            cumulative_return = (1 + sim_df.fillna(0)).cumprod()
            if portfolio_cumulative_returns is None:
                portfolio_cumulative_returns = pd.DataFrame(index=cumulative_return.index)
            portfolio_cumulative_returns[n] = cumulative_return
        
        # Set attribute to use in plotting
        self.simulated_return = portfolio_cumulative_returns
        
        # Calculate 95% confidence intervals for final cumulative returns
        self.confidence_interval = portfolio_cumulative_returns.iloc[-1, :].quantile(q=[0.025, 0.975])
        
        return portfolio_cumulative_returns
    
    def plot_simulation(self):
        """
        Visualizes the simulated stock trajectories using calc_cumulative_return method.

        """ 
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return,pd.DataFrame):
            self.calc_cumulative_return()
            
        # Use Pandas plot function to plot the return data
        plot_title = f"{self.nSim} Simulations of Cumulative {self.value_title} Trajectories Over the Next {self.num_trailing_points} Time Steps."
        # return (self.simulated_return * self.initial_value).hvplot.line(legend=False, title=plot_title, height=500, responsive=True)
        return (self.simulated_return * self.initial_value).hvplot(kind="line", legend=False, figsize=(20, 8), title=plot_title)
        # return (self.simulated_return * self.initial_value).plot(kind="line", legend=False, figsize=(20, 8), title=plot_title)
        
    def plot_distribution(self):
        """
        Visualizes the distribution of cumulative returns simulated using calc_cumulative_return method.

        """
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.calc_cumulative_return()
        
        # Use the `plot` function to create a probability distribution histogram of simulated ending prices
        # with markings for a 95% confidence interval
        plot_title = f"Distribution of Final Cumuluative {self.value_title} Across All {self.nSim} Simulations"
        # plt = self.simulated_return.iloc[-1, :].hvplot.hist(bins=10, density=True, title=plot_title, height=500, responsive=True)
        # plt = self.simulated_return.iloc[-1, :].plot(kind='hist', bins=10, density=True, title=plot_title, height=500, width=800)
        plt = (self.simulated_return * self.initial_value).iloc[-1, :].plot(kind='hist', density=True, title=plot_title, height=500, width=800)
        plt.axvline(self.confidence_interval.iloc[0], color='r')
        plt.axvline(self.confidence_interval.iloc[1], color='r')
        return plt
    
    def summarize_cumulative_return(self):
        """
        Calculate final summary statistics for Monte Carlo simulated stock data.
        
        """
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.calc_cumulative_return()
            
        metrics = (self.simulated_return * self.initial_value).iloc[-1].describe()
        ci_series = self.confidence_interval
        ci_series.index = ["95% CI Lower","95% CI Upper"]
        return metrics.append(ci_series)
