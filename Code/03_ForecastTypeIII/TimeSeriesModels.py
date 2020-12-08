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


class TimeSeriesModelUtilities:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def convert_df_to_dict(self, data_df, dict_lookup_list):
        data_dict = {}
        for dict_lookup in dict_lookup_list:
            data_dict[dict_lookup] = data_df[dict_lookup].values
        return data_dict


# Base class for the time series models - based on dictionaries of time series'
class TimeSeriesDictModel:
    
    def __init__(self, debug_level,
                x, dict_lookup_list,  # x=[list of x values], dict_lookup_list=[list of lookup values]
                values_dict, change_values_dict):  # { : [] }
        self.debug_level = debug_level
        self.x = x
        self.dict_lookup_list = dict_lookup_list
        self.values_dict = values_dict
        self.change_values_dict = change_values_dict
        self.num_input_data_points = len(x)
        self.num_dict_lookup_items = len(dict_lookup_list)

    def train(self):
        return None
    
    def predict(self):
        return None


class LinearRegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, dict_lookup_list,
                values_dict, change_values_dict,
                use_multi_stage=False):
        TimeSeriesDictModel.__init__(self, debug_level, x, dict_lookup_list, values_dict, change_values_dict)
        self.use_multi_stage = use_multi_stage

    def train(self):
        if self.use_multi_stage:
            return None  # TODO
        else:
            X = np.array(self.x).reshape(-1, 1)
            self.model_dict = {}
            for dict_lookup in self.dict_lookup_list:
                model = LinearRegression()
                y = self.values_dict[dict_lookup]
                model.fit(X, y)
                self.model_dict[dict_lookup] = model
            return True
    
    def predict(self, prediction_x_values):
        self.prediction_x_values = np.array(prediction_x_values).reshape(-1, 1)
        self.prediction_y_values = {}
        for dict_lookup in self.dict_lookup_list:
            if self.use_multi_stage:
                return None  # TODO
            else:
                model = self.model_dict[dict_lookup]
                self.prediction_y_values[dict_lookup] = model.predict(self.prediction_x_values)
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        if self.use_multi_stage:
            return None  # TODO
        else:
            r2 = {}
            for dict_lookup in self.dict_lookup_list:
                model = self.model_dict[dict_lookup]
                y = self.prediction_y_values[dict_lookup]
                r2[dict_lookup] = model.score(self.prediction_x_values, y, sample_weight=None)
            return r2
    
    def print_accuracy_metrics(self):
        if self.use_multi_stage:
            print("TODO")
        else:
            print("LinearRegressionDictModel - Accuracy Metrics Report")
            print("---------------------------------------------------")
            print("")
            accuracy_metrics = self.get_accuracy_metrics()
            for dict_lookup in self.dict_lookup_list:
                model = self.model_dict[dict_lookup]
                print(f"  Series: {dict_lookup}")
                print("")
                print("    Coefficients:")
                print(model.coef_)
                print("")
                print("    Intercepts:")
                print(model.intercept_)
                print("")
                print("    R2:")
                print(accuracy_metrics[dict_lookup])


class PolynomialRegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, dict_lookup_list,
                values_dict, change_values_dict,
                polynomial_degree=3):
        TimeSeriesDictModel.__init__(self, debug_level, x, dict_lookup_list, values_dict, change_values_dict)
        self.polynomial_degree = polynomial_degree

    def train(self):
        self.model_dict = {}
        for dict_lookup in self.dict_lookup_list:
            y = self.values_dict[dict_lookup]
            model = np.poly1d(np.polyfit(self.x, y, self.polynomial_degree))
            self.model_dict[dict_lookup] = model
        return True

    def predict(self, prediction_x_values):
        self.prediction_x_values = prediction_x_values
        self.prediction_y_values = {}
        for dict_lookup in self.dict_lookup_list:
            model = self.model_dict[dict_lookup]
            self.prediction_y_values[dict_lookup] = model(self.prediction_x_values)
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        r2 = {}
        for dict_lookup in self.dict_lookup_list:
            model = self.model_dict[dict_lookup]
            y_actual = self.values_dict[dict_lookup]
            y_predicted = self.prediction_y_values[dict_lookup][0:len(y_actual)]
            r2[dict_lookup] = r2_score(y_actual, y_predicted)
        return r2

    def print_accuracy_metrics(self):
        print("PolynomialRegressionDictModel - Accuracy Metrics Report")
        print("-------------------------------------------------------")
        print("")
        accuracy_metrics = self.get_accuracy_metrics()
        for dict_lookup in self.dict_lookup_list:
            model = self.model_dict[dict_lookup]
            print(f"  Series: {dict_lookup}")
            print("")
            print("    Coefficients:")
            print(model.coefficients)
            print("")
            print("    Roots:")
            print(model.roots)
            print("")
            print("    R2:")
            print(accuracy_metrics[dict_lookup])


class ARMARegressionDictModel(TimeSeriesDictModel):

    def __init__(self, debug_level,
                x, dict_lookup_list,
                values_dict, change_values_dict,
                order=(1,1)):
        TimeSeriesDictModel.__init__(self, debug_level, x, dict_lookup_list, values_dict, change_values_dict)
        self.order = order

    def train(self):
        self.model_dict = {}
        for dict_lookup in self.dict_lookup_list:
            y = self.values_dict[dict_lookup]
            arma_model = ARMA(y, order=self.order)
            model = arma_model.fit()
            self.model_dict[dict_lookup] = model
        return True

    def predict(self, prediction_x_values):
        self.prediction_x_values = prediction_x_values
        forecast_steps = len(self.prediction_x_values) - len(self.x)
        self.prediction_y_values = {}
        for dict_lookup in self.dict_lookup_list:
            model = self.model_dict[dict_lookup]
            self.prediction_y_values[dict_lookup] = model.forecast(steps=forecast_steps)[0]
        return self.prediction_y_values

    def get_accuracy_metrics(self):
        results = {}
        for dict_lookup in self.dict_lookup_list:
            model = self.model_dict[dict_lookup]
            results[dict_lookup] = model.summary()
        return results

    def print_accuracy_metrics(self):
        print("ARMARegressionDictModel - Accuracy Metrics Report")
        print("-------------------------------------------------------")
        print("")
        accuracy_metrics = self.get_accuracy_metrics()
        for dict_lookup in self.dict_lookup_list:
            print(f"  Series: {dict_lookup}")
            print("")
            print("    Series Model Summary:")
            print(accuracy_metrics[dict_lookup])


