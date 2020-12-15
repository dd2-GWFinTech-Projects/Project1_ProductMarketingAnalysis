from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from statsmodels.tsa.arima_model import ARMA
import enum
import pandas as pd
import numpy as np
from PlotBuildingTools import PlotBuildingTools
from IPython.display import display


class ModelType(enum.Enum):
    LinearRegressionDictModel = 0,
    PolynomialRegressionDictModel = 1,
    ARMARegressionDictModel = 2


# Base class for the time series models - based on dictionaries of time series'
class TimeSeriesDictModel:
    
    def __init__(self, debug_level,
                x, series_key_list,  # x=[list of x values], series_key_list=[list of lookup values]
                values_dict, change_values_dict):  # { : [] }
        self.debug_level = debug_level
        self.x = x
        self.series_key_list = series_key_list
        self.values_dict = values_dict
        self.change_values_dict = change_values_dict
        self.num_input_data_points = len(x)
        self.num_series_key_items = len(series_key_list)

    def train(self):
        return None
    
    def predict(self, prediction_x_values):
        return None


class LinearRegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, series_key_list,
                values_dict, change_values_dict,
                use_multi_stage=False):
        TimeSeriesDictModel.__init__(self, debug_level, x, series_key_list, values_dict, change_values_dict)
        self.use_multi_stage = use_multi_stage

    def train(self):
        if self.use_multi_stage:
            return None  # TODO
        else:
            X = np.array(self.x).reshape(-1, 1)
            self.model_dict = {}
            for series_key in self.series_key_list:
                model = LinearRegression()
                # print(f"LinearRegressionDictModel - self.values_dict {self.values_dict}")
                # print(f"LinearRegressionDictModel - series_key {series_key}")
                y = self.values_dict[series_key]
                # print(f"LinearRegressionDictModel - X {X}")
                # print(f"LinearRegressionDictModel - y {y}")
                model.fit(X, y)
                self.model_dict[series_key] = model
            return True
    
    def predict(self, prediction_x_values):
        self.prediction_x_values = np.array(prediction_x_values).reshape(-1, 1)
        self.prediction_y_values = {}
        for series_key in self.series_key_list:
            if self.use_multi_stage:
                return None  # TODO
            else:
                model = self.model_dict[series_key]
                # print(f"LinearRegressionDictModel.predict() - self.prediction_x_values {self.prediction_x_values}")
                # print(f"LinearRegressionDictModel.predict() - model.predict(self.prediction_x_values) {model.predict(self.prediction_x_values)}")
                self.prediction_y_values[series_key] = model.predict(self.prediction_x_values)
        # print(f"LinearRegressionDictModel.predict() - self.prediction_y_values {self.prediction_y_values}")
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        if self.use_multi_stage:
            return None  # TODO
        else:
            r2 = {}
            for series_key in self.series_key_list:
                model = self.model_dict[series_key]
                y = self.prediction_y_values[series_key]
                r2[series_key] = model.score(self.prediction_x_values, y, sample_weight=None)
            return r2
    
    def print_accuracy_metrics(self):
        if self.use_multi_stage:
            print("TODO")
        else:
            print("LinearRegressionDictModel - Accuracy Metrics Report")
            print("---------------------------------------------------")
            print("")
            accuracy_metrics = self.get_accuracy_metrics()
            for series_key in self.series_key_list:
                model = self.model_dict[series_key]
                print(f"  Series: {series_key}")
                print("")
                print("    Coefficients:")
                print(model.coef_)
                print("")
                print("    Intercepts:")
                print(model.intercept_)
                print("")
                print("    R2:")
                print(accuracy_metrics[series_key])


class PolynomialRegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, series_key_list,
                values_dict, change_values_dict,
                polynomial_degree=3):
        TimeSeriesDictModel.__init__(self, debug_level, x, series_key_list, values_dict, change_values_dict)
        self.polynomial_degree = polynomial_degree

    def train(self):
        self.model_dict = {}
        for series_key in self.series_key_list:
            y = self.values_dict[series_key]
            model = np.poly1d(np.polyfit(self.x, y, self.polynomial_degree))
            self.model_dict[series_key] = model
        return True

    def predict(self, prediction_x_values):
        self.prediction_x_values = prediction_x_values
        self.prediction_y_values = {}
        for series_key in self.series_key_list:
            model = self.model_dict[series_key]
            self.prediction_y_values[series_key] = model(self.prediction_x_values)
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        r2 = {}
        for series_key in self.series_key_list:
            model = self.model_dict[series_key]
            y_actual = self.values_dict[series_key]
            y_predicted = self.prediction_y_values[series_key][0:len(y_actual)]
            r2[series_key] = r2_score(y_actual, y_predicted)
        return r2

    def print_accuracy_metrics(self):
        print("PolynomialRegressionDictModel - Accuracy Metrics Report")
        print("-------------------------------------------------------")
        print("")
        accuracy_metrics = self.get_accuracy_metrics()
        for series_key in self.series_key_list:
            model = self.model_dict[series_key]
            print(f"  Series: {series_key}")
            print("")
            print("    Coefficients:")
            print(model.coefficients)
            print("")
            print("    Roots:")
            print(model.roots)
            print("")
            print("    R2:")
            print(accuracy_metrics[series_key])


class ARMARegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, series_key_list,
                values_dict, change_values_dict,
                order=(1,1)):
        TimeSeriesDictModel.__init__(self, debug_level, x, series_key_list, values_dict, change_values_dict)
        self.order = order

    def train(self):
        self.model_dict = {}
        for series_key in self.series_key_list:
            y = self.values_dict[series_key]
            arma_model = ARMA(y, order=self.order)
            model = arma_model.fit()
            self.model_dict[series_key] = model
        return True

    def predict(self, prediction_x_values):
        self.prediction_x_values = prediction_x_values
        forecast_steps = len(self.prediction_x_values) - len(self.x)
        self.prediction_y_values = {}
        for series_key in self.series_key_list:
            model = self.model_dict[series_key]
            self.prediction_y_values[series_key] = model.forecast(steps=forecast_steps)[0]
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        results = {}
        for series_key in self.series_key_list:
            model = self.model_dict[series_key]
            results[series_key] = model.summary()
        return results

    def print_accuracy_metrics(self):
        print("ARMARegressionDictModel - Accuracy Metrics Report")
        print("-------------------------------------------------------")
        print("")
        accuracy_metrics = self.get_accuracy_metrics()
        for series_key in self.series_key_list:
            print(f"  Series: {series_key}")
            print("")
            print("    Series Model Summary:")
            print(accuracy_metrics[series_key])


class TimeSeriesModelUtilities:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    # --------------------------------------------------------------------------
    # Series Map - DataFrame Conversions
    # --------------------------------------------------------------------------

    def convert_df_to_series_map(self, data_df, series_key_list):
        data_dict = {}
        for series_key in series_key_list:
            data_dict[series_key] = data_df[series_key].values
        return data_dict
    
    def convert_series_map_to_df(self, data_series_map, index=None):

        series_key_list = list(data_series_map.keys())
        value_length = len(data_series_map[series_key_list[0]])

        # Build empty DataFrame
        if index is None:
            index = range(0, value_length)
        data_df = pd.DataFrame(index)

        # Append each series as a column
        for series_key in series_key_list:
            data_df[str(series_key)] = data_series_map[series_key]

        return data_df

    # def (self, data_series_map, series_key_list, index=None):

    #     value_length = len(data_series_map[series_key_list[0]])

    #     if index is None:
    #         index = range(0, value_length)

    #     data_map = {}

    #     # Populate with each series data
    #     for series_key in series_key_list:
            
    #         # Build empty dataframe
    #         data_df = pd.DataFrame(index=index)

    #         # Populate with each simulation run
    #         for run_index in self.num_simulation:
    #             data_df[run_index] = data_series_map[run_index][series_key]

    #         data_map[series_key] = data_df

    # def extract_simulation_values_to_df(self, simulation_values):

    #     # Populate each series with simulated runs
    #     series_simulation_df_map = {}
    #     for series_key in self.series_key_list:
            
    #         # Initialize empty DataFrame
    #         series_simulation_df_map[series_key] = pd.DataFrame(index = self.forward_value_predictor.all_x_values)

    #         # Populate with simulated runs
    #         for run_index in self.num_simulation:
    #             series_simulation_df_map[series_key][run_index] = simulation_values[run_index][series_key]

    #     return series_simulation_df_map

    # --------------------------------------------------------------------------
    # Series Map Operations
    # --------------------------------------------------------------------------

    def init_series_map(self, series_key_list):
        series_lookup_map = { }
        for series_key in series_key_list:
            series_lookup_map[series_key] = []
        return series_lookup_map

    def split_series_map(self, map, index, debug=False):

        series_key_list = list(map.keys())

        # if debug:
        #     print(f"split_series_map - map {map}")
        #     print(f"split_series_map - index {index}")

        #     print(f"split_series_map - series_length {len(map[series_key_list[0]])}")
        #     print(f"split_series_map - map1 {map[series_key_list[0]][0:index]}")
        #     print(f"split_series_map - map2 {map[series_key_list[0]][index:len(map[series_key_list[0]])]}")

        map1 = self.init_series_map(series_key_list)
        map2 = self.init_series_map(series_key_list)
        
        series_length = len(map[series_key_list[0]])

        for series_key in series_key_list:
            map1[series_key] = map[series_key][0:index]
            map2[series_key] = map[series_key][index:series_length]

        return (map1, map2)

    def join_series_maps(self, map1, map2):

        series_key_list = list(map1.keys())

        map = self.init_series_map(series_key_list)
        
        for series_key in series_key_list:
            # print(f"join_series_maps - series_key {series_key}")
            # print(f"join_series_maps - map1 {map1}")
            # print(f"join_series_maps - map2 {map2}")
            map[series_key] = np.concatenate(( map1[series_key], map2[series_key] ))

        return map

    # --------------------------------------------------------------------------
    # Model Builder
    # --------------------------------------------------------------------------

    def build_model(self, model_type,
                x, series_key_list,
                values_dict, change_values_dict,
                opts_dict):

        if model_type == ModelType.LinearRegressionDictModel:

            # print(f"build_model - x {x}")
            # print(f"build_model - values_dict {values_dict}")

            return LinearRegressionDictModel(
                debug_level=self.debug_level,
                x=x, series_key_list=series_key_list,
                values_dict=values_dict,
                change_values_dict=change_values_dict,
                use_multi_stage=opts_dict["use_multi_stage"])

        elif model_type == ModelType.PolynomialRegressionDictModel:

            return PolynomialRegressionDictModel(
                debug_level=self.debug_level,
                x=x, series_key_list=series_key_list,
                values_dict=values_dict,
                change_values_dict=change_values_dict,
                polynomial_degree=opts_dict["degree"])

        elif model_type == ModelType.ARMARegressionDictModel:

            return ARMARegressionDictModel(
                debug_level=self.debug_level,
                x=x, series_key_list=series_key_list,
                values_dict=values_dict,
                change_values_dict=change_values_dict,
                order=opts_dict["order"])

        else:

            return None


class TimeSeriesModelPredictionPreviewUtilities:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level
        self.time_series_model_utilities = TimeSeriesModelUtilities()
        self.plot_building_tool = PlotBuildingTools(debug_level)

    def generate_prediction_preview(self, model_type,
                x, series_key_list,
                values_dict_df, change_values_dict_df,
                opts_dict,
                prediction_x_values):

        # Convert data types
        values_dict = self.time_series_model_utilities.convert_df_to_series_map(values_dict_df, series_key_list)
        change_values_dict = self.time_series_model_utilities.convert_df_to_series_map(change_values_dict_df, series_key_list)
        series_key_list_prediction_names = [(lambda x: "Predicted_" + str(x))(x) for x in series_key_list]

        # Build, train, predict
        model__values_dict = self.time_series_model_utilities.build_model(model_type, 
                x, series_key_list,
                values_dict, change_values_dict,
                opts_dict)

        model__values_dict.train()
        model_predictions__values_dict = model__values_dict.predict(prediction_x_values)
        
        # Tabulate
        model_predictions__values_dict__df = pd.DataFrame(model_predictions__values_dict, index=prediction_x_values)
        model_predictions__values_dict__df.columns = series_key_list_prediction_names
        display(model_predictions__values_dict__df)
        
        # Display accuracy metrics
        display(model__values_dict.get_accuracy_metrics())
        display(model__values_dict.print_accuracy_metrics())
        
        # Plot
        merged_predictions_df__values_dict = pd.concat([values_dict_df, model_predictions__values_dict__df], axis="columns", join="outer")
        display(merged_predictions_df__values_dict)
        return self.plot_building_tool.generate_plot__hvplot_line(merged_predictions_df__values_dict,
            title="Macro Customer Behavior Counts", xlabel="Year Index", ylabel="Nbr. Customers",
            width=900, height=300)
