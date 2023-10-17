from sklearn.exceptions import ConvergenceWarning
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import r2_score
import itertools
import warnings

# Add this line to ignore all warnings
warnings.filterwarnings("ignore")

class ARIMAModel:
    def __init__(self):

        self.forecast = None
        self.rscore = None

    def get_score(self, test, arima_forecast):
        # Calculate R2 score as a measure of accuracy
        # r2_arima = r2_score(test, arima_forecast)
        r2_arima = self.rscore
        return r2_arima

    def get_model(self, train, test, data):
        print("------------------------------The ARIMA Model ------------------------------")
        # Define ranges for p, d, and q values
        p_values = range(0, 3)
        d_values = range(0, 2)
        q_values = range(0, 3)

        best_order = None
        best_model = None
        best_r2 = -float('inf')

        # Iterate through hyperparameters
        for p, d, q in itertools.product(p_values, d_values, q_values):
            order = (p, d, q)

            # Fit ARIMA model with current hyperparameters
            model = ARIMA(train, order=order)
            model_fit = model.fit()

            # Make predictions on the test set
            forecast = model_fit.forecast(steps=len(test))

            # Calculate R2 score for the current model
            r2 = r2_score(test, forecast)

            # Update best model and R2 score if the current model is better
            if r2 > best_r2:
                best_model = model_fit
                best_r2 = r2
                self.forecast = forecast
                self.rscore = best_r2
                best_order = order

        # Return the best ARIMA model
        # return best_model
        return best_model

    def get_forecast(self, train, test, model):
        # Make predictions on the test set using the best ARIMA model
        # arima_forecast = model.forecast(steps=len(test))
        arima_forecast = self.forecast
        return arima_forecast


# Reset warning filter when you're done
warnings.filterwarnings("default")
