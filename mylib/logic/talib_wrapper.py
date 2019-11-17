import talib as ta
import numpy as np


class TAlibWrapper:

    def get_technicals_of_series(self, indivations):
        result = ta.SMA(indivations, timeperiod=5)
        result = np.vstack((result, ta.SMA(indivations, timeperiod=14)))
        result = np.vstack((result, ta.MAMA(indivations)))
        result = np.vstack((result, ta.BBANDS(indivations)))
        result = np.vstack((result, ta.APO(indivations)))
        result = np.vstack((result, ta.CMO(indivations)))
        result = np.vstack((result, ta.MACD(indivations)))
        result = np.vstack((result, ta.MOM(indivations)))
        result = np.vstack((result, ta.ROC(indivations)))
        result = np.vstack((result, ta.RSI(indivations)))
        result = np.vstack((result, ta.HT_TRENDMODE(indivations)))
        result = np.vstack((result, ta.LINEARREG(indivations)))
        result = result[:, ~np.isnan(result).any(axis=0)]
        result = result.T
        return result

