import matplotlib.pyplot as plt
import pandas as pd


class PlotManager:
    def plot_timeseries_df(self, df: pd.DataFrame):
        answer = df.set_index(['Date'])
        answer.plot()
        plt.show()