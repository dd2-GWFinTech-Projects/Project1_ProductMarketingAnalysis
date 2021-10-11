# Import libraries and dependencies
import numpy as np
import pandas as pd
import os
import datetime as dt
import pytz

class MCSimulation_Generic:
    """
    A Python class for runnning Monte Carlo simulation on portfolio price data. 
    
    ...
    
    Attributes
    ----------
    portfolio_data : pandas.DataFrame
        portfolio dataframe
    weights: list(float)
        portfolio investment breakdown
    nSim: int
        number of samples in simulation
    num_trailing_points: int
        number of trading days to simulate
    simulated_return : pandas.DataFrame
        Simulated data from Monte Carlo
    confidence_interval : pandas.Series
        the 95% confidence intervals for simulated final cumulative returns
        
    """
    
    def __init__(self,
        value_title,
        value_list,
        num_simulation=1000, num_trailing_points=50,
        scale_results=True,
        allow_negative_returns=True
        ):
        """
        Constructs all the necessary attributes for the MCSimulation object.

        Parameters
        ----------
        value_list: pandas.DataFrame
            DataFrame containing values for each time instant.
        num_simulation: int
            Number of simulation samples. DEFAULT: 1000 simulation samples
        num_trailing_points: int
            Number of trading days to simulate. DEFAULT: 252 days (1 year of business days)
        """

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

            # Simulate the returns for each trading day
            for i in range(self.num_trailing_points):
    
                # Calculate the simulated price using the last price within the list

                # print(f"simvals type {type(simvals)}")

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
