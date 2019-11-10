# from keras.models import Sequential
# from keras.layers import Dense, Activation
from back_system.shared import SharedLogic
from back_system.quandl_manager import QuandlManager
import numpy as np


class IndicateDenceModel:
    def create_dataset(self, objective, term, test_rate=0.3):
        df = QuandlManager().get_indicative_histoty()
        df = df.set_index(['Date'])
        y = df.iloc[term:].loc[:, objective].values
        X = []
        mean, std = df.mean(axis=0), df.std(axis=0)
        standardized = (df - mean) / std
        for i in range(0, len(df)-term):
            work = standardized.iloc[i: i+term].values.flatten()
            X.append(work)
        print(f"y shape:{np.shape(y)} x shape:{np.shape(X)}")


if __name__ == "__main__":
    SharedLogic.initialize('1234')
    SharedLogic.initialize_config()
    SharedLogic.initialize_db()
    idm = IndicateDenceModel()
    idm.create_dataset('GBPJPY', 14)
