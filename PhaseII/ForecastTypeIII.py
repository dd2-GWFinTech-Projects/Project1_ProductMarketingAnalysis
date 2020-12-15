from IPython import get_ipython

# %%
# TODO
# [X] Provide gut checks.
# [ ] Look into existing MC implementations!!!
# [ ] Model regional effects (i.e. customer's state) as [classifiers]!!!

# %% [markdown]
# # Initialize

# %%
# Options

## Debugging level
debug_level = 0


# %%
# Initialize framework
from imports import *
constants, tools = init_processing(debug_level)
pn.extension("plotly")
hv.extension('bokeh', 'matplotlib')
get_ipython().run_line_magic('matplotlib', 'inline')


# %%
# Import all preprocessed data
invoice_data_by_customer            = pd.read_pickle(constants.PREPROCESSED_INVOICE_CUSTOMER_FILE_PATH)
invoice_data_by_service_start       = pd.read_pickle(constants.PREPROCESSED_INVOICE_SERVICEDATE_FILE_PATH)
invoice_data_by_invoice_date        = pd.read_pickle(constants.PREPROCESSED_INVOICE_INVOICEDATE_FILE_PATH)
forecast                            = pd.read_pickle(constants.PREPROCESSED_FORECAST_CLEANED_FILE_PATH)
revenue2020A                        = pd.read_pickle(constants.PREPROCESSED_REVENUE2020A_CLEANED_FILE_PATH)

invoice_data_by_customer.shape


# %%
# pwd = os.getcwd()
# sys.path.append(pwd + "../lib2")
# # sys.path.append("../lib2")
# print(sys.path)

# Specialized imports
from UpgradeSequenceDataStructures import UpgradeType
from UpgradeSequenceDataStructures import CustomerBehaviorObservations
from UpgradeSequenceDataStructures import CustomerBehaviorClassifications

from MCForecastTools_MacroCustomerSales_DataStructures import MacroCustomerBehaviorNumbers

from MCForecastTools_MacroCustomerSales import MacroCustomerSales_HistoricalAnalysis
from MCForecastTools_MacroCustomerSales import ForwardPredictor
from MCForecastTools_MacroCustomerSales import PredictionFuzzer
from MCForecastTools_MacroCustomerSales import MCSimulation_MacroCustomerSales

tool_historical = MacroCustomerSales_HistoricalAnalysis()

from TimeSeriesModels import ModelType
from TimeSeriesModels import TimeSeriesModelUtilities
from TimeSeriesModels import TimeSeriesModelPredictionPreviewUtilities
from TimeSeriesModels import TimeSeriesDictModel
from TimeSeriesModels import LinearRegressionDictModel
from TimeSeriesModels import PolynomialRegressionDictModel
from TimeSeriesModels import ARMARegressionDictModel

prediction_preview_tool = TimeSeriesModelPredictionPreviewUtilities()
time_series_model_utilities = TimeSeriesModelUtilities()

# %% [markdown]
# # Best/Worst Bounds Simulation

# %%
# TODO

# %% [markdown]
# # Macro Customer Behavior Counts Simulation
# %% [markdown]
# ## Data Preparation

# %%
year_list = [ 2015, 2016, 2017, 2018, 2019, 2020 ]
classification_list = [ CustomerBehaviorClassifications.New, CustomerBehaviorClassifications.Continued_Loyal, CustomerBehaviorClassifications.Continued_AtRisk, CustomerBehaviorClassifications.Continued_Nominal, CustomerBehaviorClassifications.Dropped ]


# %%
# Macro customer counts - TODO these are good numbers from spreadsheet analysis.
macro_customer_behavior_counts_sequence = pd.DataFrame({
    CustomerBehaviorClassifications.New: [ 8, 27, 31, 38, 69, 218 ],
    CustomerBehaviorClassifications.Continued_Loyal: [ 0, 5, 8, 21, 15, 33 ],
    CustomerBehaviorClassifications.Continued_AtRisk: [ 0, 0, 0, 0, 0, 0 ],
    CustomerBehaviorClassifications.Continued_Nominal: [ 0, 0, 0, 0, 0, 0 ],
    CustomerBehaviorClassifications.Dropped: [ 0, 16, 21, 18, 16, 20 ]
}, index=year_list)

# Macro customer counts - fractional change
macro_customer_behavior_counts_change_sequence = macro_customer_behavior_counts_sequence.pct_change().replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)

# Macro customer counts - rolling std
macro_customer_behavior_counts_std_sequence = tool_historical.compute_rolling_std(macro_customer_behavior_counts_sequence, 3).replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)

# Macro customer counts - fractional change rolling std
macro_customer_behavior_counts_change_std_sequence = tool_historical.compute_rolling_std(macro_customer_behavior_counts_change_sequence, 3).replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)


# %%
# Display tabulated customer behavior counts data
[
    display(macro_customer_behavior_counts_sequence),
    display(macro_customer_behavior_counts_change_sequence),
    display(macro_customer_behavior_counts_std_sequence),
    display(macro_customer_behavior_counts_change_std_sequence)
]


# %%
# Avg annual sales - TODO Made-up numbers
macro_customer_avg_annual_sales_sequence = pd.DataFrame({
    CustomerBehaviorClassifications.New: [ 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0 ],
    CustomerBehaviorClassifications.Continued_Loyal: [ 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0 ],
    CustomerBehaviorClassifications.Continued_AtRisk: [ 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0 ],
    CustomerBehaviorClassifications.Continued_Nominal: [ 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0 ],
    CustomerBehaviorClassifications.Dropped: [ 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0 ]
}, index=year_list)

# Avg annual sales - fractional change
macro_customer_avg_annual_sales_change_sequence = macro_customer_avg_annual_sales_sequence.pct_change().replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)

# Avg annual sales - rolling std deviation
macro_customer_avg_annual_sales_std_sequence = tool_historical.compute_rolling_std(macro_customer_avg_annual_sales_sequence, 3).replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)

# Avg annual sales - change rolling std deviation
macro_customer_avg_annual_sales_change_std_sequence = tool_historical.compute_rolling_std(macro_customer_avg_annual_sales_change_sequence, 3).replace(np.nan, 0).replace(np.inf, 1.0).replace(-np.inf, -1.0)


# %%
# Display tabulated avg. sales data
[
    display(macro_customer_avg_annual_sales_sequence),
    display(macro_customer_avg_annual_sales_change_sequence),
    display(macro_customer_avg_annual_sales_std_sequence),
    display(macro_customer_avg_annual_sales_change_std_sequence)
]


# %%


# %% [markdown]
# ## Predict data to check before running inside Monte-Carlo: macro_customer_behavior_counts_sequence

# %%
# Generate x values for prediction
historical_and_prediction_year_list = [ 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 ]

# Generate x axis points for plotting the models
years_intermediate_points_for_plotting = np.linspace(year_list[0], year_list[-1], 100)


# %%



# %%
# LinearRegressionDictModel
prediction_preview_tool.generate_prediction_preview(ModelType.LinearRegressionDictModel, 
    year_list, classification_list,
    macro_customer_behavior_counts_sequence, macro_customer_behavior_counts_change_sequence,
    { "use_multi_stage": False },
    historical_and_prediction_year_list)


# %%
# PolynomialRegressionDictModel
prediction_preview_tool.generate_prediction_preview(ModelType.PolynomialRegressionDictModel, 
    year_list, classification_list,
    macro_customer_behavior_counts_sequence, macro_customer_behavior_counts_change_sequence,
    { "degree": 3 },
    historical_and_prediction_year_list)


# %%
# ARMARegressionDictModel
# TODO Unable with only 5 data points. Error: "ValueError: The model specification cannot be estimated. The model contains 5 regressors (0 trend, 0 seasonal, 5 lags) but after adjustment for hold_back and creation of the lags, there are only 1 data points available to estimate parameters."
# prediction_preview_tool.generate_prediction_preview(ModelType.ARMARegressionDictModel, 
#     year_list, classification_list,
#     macro_customer_behavior_counts_sequence, macro_customer_behavior_counts_change_sequence,
#     { "order": (1, 1) },
#     historical_and_prediction_year_list)


# %%


# %% [markdown]
# ## Plots the simulation input data

# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_behavior_counts_sequence,
    title="Macro Customer Behavior Counts", xlabel="Year Index", ylabel="Nbr. Customers",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_behavior_counts_change_sequence,
    title="Macro Customer Behavior Counts - Fractional Change", xlabel="Year Index", ylabel="Fractional Change in Nbr. Customers",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_behavior_counts_std_sequence,
    title="Macro Customer Behavior Counts - Standard Deviation", xlabel="Year Index", ylabel="std(Nbr. Customers)",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_behavior_counts_change_std_sequence,
    title="Macro Customer Behavior Counts - Fractional Change Standard Deviation", xlabel="Year Index", ylabel="std(Fractional Change in Nbr. Customers)",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_avg_annual_sales_sequence,
    title="Macro Customer Avg. Annual Sales", xlabel="Year Index", ylabel="Avg. Annual Sales",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_avg_annual_sales_change_sequence,
    title="Macro Customer Avg. Annual Sales - Standard Deviation", xlabel="Year Index", ylabel="Fractional Change of Avg. Annual Sales",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_avg_annual_sales_std_sequence,
    title="Macro Customer Avg. Annual Sales - Fractional Change", xlabel="Year Index", ylabel="std(Avg. Annual Sales)",
    width=1400, height=500)


# %%
tools.tool_plot_building.generate_plot__hvplot_line(macro_customer_avg_annual_sales_change_std_sequence,
    title="Macro Customer Avg. Annual Sales - Fractional Change Standard Deviation", xlabel="Year Index", ylabel="std(Fractional Change of Avg. Annual Sales)",
    width=1400, height=500)


# %%


# %% [markdown]
# ## Build simulations

# %%
# Configure MC simulation

forward_value_predictor = ForwardPredictor(
    debug_level = 0,
    all_x_values = historical_and_prediction_year_list,
    series_key_list = classification_list,
    values_dict = time_series_model_utilities.convert_df_to_series_map(macro_customer_behavior_counts_sequence, classification_list),
    model_type = ModelType.LinearRegressionDictModel,
    opts_dict = { "use_multi_stage": False },
    min_index = 2)

forward_std_predictor = ForwardPredictor(
    debug_level = 0,
    all_x_values = historical_and_prediction_year_list,
    series_key_list = classification_list,
    values_dict = time_series_model_utilities.convert_df_to_series_map(macro_customer_behavior_counts_std_sequence, classification_list),
    model_type = ModelType.LinearRegressionDictModel,
    opts_dict = { "use_multi_stage": False },
    min_index = 2)

prediction_fuzzer = PredictionFuzzer()

simulator = MCSimulation_MacroCustomerSales(
    debug_level=0,
    series_key_list = classification_list,
    forward_value_predictor = forward_value_predictor,
    forward_std_predictor = forward_std_predictor,
    prediction_fuzzer = prediction_fuzzer,
    num_simulation = 100,
    simulation_value_title = "Customer Sales Counts",
    num_prediction_time_steps = len(historical_and_prediction_year_list) - len(year_list))


# %%



# %%
# values=[1, 2, 3, 4]

# # series_length = len(values)
# # split_index = series_length - 1
# # values[split_index:series_length]

# # np.quantile(np.array(values), q=[0.025, 0.975])

# df = pd.DataFrame(index=values)

# df["col1"] = values
# df

# df2 = pd.DataFrame(index=values)
# df2["col1"] = [3, 4, 3, 7]

# plt = pd.DataFrame(index=values).plot()
# plt.plot(df)
# plt.plot(df2)


# %%



# %%



# %%
# Run the simulation
simulator.run()


# %%
# a=[ 46.,  65.,  84., 103., 122., 141., 160.]
# b=[ 10., 15., 20., 25., 30., 35., 40.]
# # a=np.array([ 46.,  65.,  84., 103., 122., 141., 160.])
# # b=np.array([10., 15., 20., 25., 30., 35., 40.])
# np.concatenate((a, b))


# %%
# Post-process
simulator.extract_last_values()
simulator.compute_statistics()


# %%
# Plot the results
simulator.plot_simulation()

results_distribution_plot_map = simulator.plot_distribution()


# %%



# %%
# Save tabulated results
simulation_values = simulator.simulation_values
metrics_map = simulator.summarize_ending_simulation_results()

metrics_map


# %%



# %%



# %%
# TODO These are made-up numbers
# macro_customer_behavior_counts_list = [
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 8,
#             nbr_continued_loyal_customers = 0,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 0,
#             year = 2015),
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 2,
#             nbr_continued_loyal_customers = 2,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 1,
#             year = 2016),
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 3,
#             nbr_continued_loyal_customers = 5,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 2,
#             year = 2017),
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 5,
#             nbr_continued_loyal_customers = 15,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 3,
#             year = 2018),
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 10,
#             nbr_continued_loyal_customers = 30,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 4,
#             year = 2019),
#         MacroCustomerBehaviorCounts(
#             nbr_new_customers = 190,
#             nbr_continued_loyal_customers = 60,
#             nbr_continued_at_risk_customers = 0,
#             nbr_continued_nominal_customers = 0,
#             nbr_dropped_customers = 10,
#             year = 2020)
# ]

# macro_customer_avg_annual_sales_list = [
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2015),
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2016),
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2017),
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2018),
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2019),
#         MacroCustomerAverageAnnualSales(
#             avg_annual_sales_new_customers = 5000.0,
#             avg_annual_sales_continued_loyal_customers = 5000.0,
#             avg_annual_sales_continued_at_risk_customers = 5000.0,
#             avg_annual_sales_continued_nominal_customers = 5000.0,
#             avg_annual_sales_dropped_customers = 1000.0,
#             year = 2020)
# ]

# %% [markdown]
# # (Old) Simple Generic Simulation

# %%
# historical_data = atlas.reset_index().set_index("Service Start").sort_index(ascending=True)

# historical_data_invoice_amount = historical_data.groupby("Service Start").sum()["Invoice Amount"]
# historical_data_invoice_count = historical_data.groupby("Service Start").count()["Invoice Amount"]

# # Critical
# historical_data_invoice_amount_cumulative = historical_data_invoice_amount.cumsum()
# historical_data_invoice_count_cumulative = historical_data_invoice_count.cumsum()

# # Extra
# historical_data_invoice_mean = historical_data.groupby("Service Start").mean()["Invoice Amount"]
# historical_data_nbr_users = historical_data.groupby("Service Start").sum()["Number of Users"]
# historical_data_nbr_customers = historical_data.groupby("Service Start").count()["Customers"]

# historical_data_nbr_users_cumulative = historical_data_nbr_users.cumsum()
# historical_data_nbr_customers_cumulative = historical_data_nbr_customers.cumsum()


# %%
# historical_data_invoice_amount_cumulative.tail(20)


# %%
# mc = MCSimulation_Generic(
#     value_title="Invoice Amount",
#     value_list = historical_data_invoice_amount_cumulative,
#     num_simulation=1000,
#     num_trailing_points = 10,
#     scale_results=True,
#     allow_negative_returns = True
# )

# mc.calc_cumulative_return()


# %%
# mc.plot_simulation()


# %%
# # mc.plot_distribution()
# mc.simulated_return.iloc[-1, :]
# mc.simulated_return.iloc[-1, :].plot(kind='hist', title="")
# # mc.simulated_return.iloc[-1, :].plot(kind='hist', bins=10, density=True, title="", height=500, width=800)


# %%
# mc.summarize_cumulative_return()


# %%
# historical_data_invoice_amount_cumulative.hvplot.line()


# %%
# historical_data_invoice_count_cumulative.hvplot.line()


# %%
# historical_data_nbr_users_cumulative.hvplot.line()


# %%
# historical_data_nbr_customers_cumulative.hvplot.line()


# %%



# %%
# test
# df = pd.DataFrame({'A': [0, 100, 110, 115, 120], 'B': [0, 100, 110, 115, 120]}).T
# df.rolling(window=3, axis=1).std()

df = pd.DataFrame({'A': [0, 100, 110, 115, 120], 'B': [0, 100, 110, 115, 120]})
df2 = df.rolling(window=3).std()
df2
# df2.T.to_dict()


# %%



