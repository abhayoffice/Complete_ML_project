from sklearn.metrics import r2_score
from pmdarima import auto_arima
import pandas as pd

class ARIMAModel:
    def __init__(self, config):
        self.config = config

    def get_score(self, test, arima_forecast):
        arima_forecast_series = pd.Series(arima_forecast, index=test.index)
        r2_arima = r2_score(test[self.config["target_column"]], arima_forecast_series)
        return r2_arima

    def get_model(self, train, test):
        print("------------------------------The Arima Model ------------------------------")
        arima_model = auto_arima(
            train[self.config["target_column"]],
            seasonal=False,
            stepwise=True,
            trace=False
        )
        return arima_model

    def get_forecast(self, train, test, model):
        arima_forecast = model.predict(n_periods=len(test))
        return arima_forecast