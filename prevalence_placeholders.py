import numpy as np
import sys
from scipy.integrate import odeint
from model_data.zip_codes import ZIP_CODES


class PlaceholderZipCodePrevalenceModel():
    model_type = "prevalence"
    model_name = "placeholder-zip-code-prevalence-model"
    model_id = "V0.01_2020-05-02"
    is_forecast_model = True
    input_models = []

    def __init__(self):
        self.zip_codes = ZIP_CODES
        self.local_prevalence = self.prevalence_over_time(365*2)

    def prevalence_over_time(self, num_days: int):
        # From: https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/

        # Total population, N.
        N = 1000
        # Initial number of infected and recovered individuals, I0 and R0.
        I0, R0 = 50, 50
        # Everyone else, S0, is susceptible to infection initially.
        S0 = N - I0 - R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        beta, gamma = 0.2, 1. / 8
        # A grid of time points (in days)
        t = np.linspace(0, num_days, num_days)

        # The SIR model differential equations.
        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt

        # Initial conditions vector
        y0 = S0, I0, R0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T
        return I / N

    def zip_code_prevalence(self, dates: list, inputs_sample: dict) -> list:
        prevalences = []
        for t_i, date in enumerate(dates):
            prevalences.append({})
            for z in self.zip_codes:
                prevalences[-1][z] = round(self.local_prevalence[t_i] * (1.0 + (np.random.rand() * 0.1 - 0.05)), 4)
        return prevalences

    def single_draw_from_model(self, dates: list, inputs_sample: dict) -> list:
        return self.zip_code_prevalence(dates, inputs_sample)


if __name__ == "__main__":

    dates = sys.argv[1]
    inputs_sample = sys.argv[2]

    prevalence_model = PlaceholderZipCodePrevalenceModel()
    prevalence_model.single_draw_from_model()
