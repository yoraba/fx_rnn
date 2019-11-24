from back_system.shared import SharedContext
from back_system.api.ta_api import TAlib_API
from back_system.constants import Constants
from mylib.ai.keras_wrapper import RNNContext, RNNWrapper
from mylib.logic.talib_wrapper import TAlibWrapper
import numpy as np


class KerasAPI:

    def __init__(self, context: SharedContext):
        self._context = context
        rnn_context = RNNContext()
        rnn_context.window_size = context.Config.General.window_size
        rnn_context.tensor_board_dir = Constants.TENSOR_BOARD_DIR
        rnn_context.model_dir = Constants.MODEL_DIR
        self.rnn_wrapper = RNNWrapper(rnn_context)

    def create_data(self):
        api = TAlib_API(self._context)
        data = api.get_technicals()
        data = self.rnn_wrapper.preprocess(data)
        data = TAlibWrapper().add_high_low_data(data)
        Xall, yall = self.rnn_wrapper.make_data_and_label(data)
        partition = round(len(yall) * 0.7)
        Xtrain, ytrain = Xall[:partition], yall[:partition]
        Xtest, ytest = Xall[partition:], yall[:partition]
        return Xall, yall, Xtrain, ytrain, Xtest, ytest

    def fit(self):
        (Xall, yall, Xtrain, ytrain, Xtest, ytest) = self.create_data()
        model = self.rnn_wrapper.create_basic_lstm_model(Xtrain)
        result = self.rnn_wrapper.fit(model, Xtrain, ytrain)
        self.rnn_wrapper.save2file(result)

    def predict(self):
        #self.fit()
        model = self.rnn_wrapper.loadModelFfile()
        (Xall, yall, Xtrain, ytrain, Xtest, ytest) = self.create_data()
        prediction = model.predict(Xall)
        high_row_score = []
        for i in range(np.shape(yall)[1]):
            match, total  = self.rnn_wrapper.high_low_probavility_score_with_border(yall, prediction, i)
            high_row_score.append(f" {match} / {total} {(match + 0.0001) /(total + 0.0001)}%")
            # self.save_plot(yall[:, i], prediction[:, i], f"high low prob top 100:{i}")
        return high_row_score

    def save_plot(self, answer, prediction, name):
        import matplotlib.pyplot as plt
        import io
        x = range(100)
        y = answer[-100:]
        pred_y = prediction[-100:]
        plt.ylim(-0.1, 1.1)
        plt.plot(x, [0.5]*len(y), label='border')
        plt.plot(x, y, label='answer')
        plt.plot(x, pred_y, label='prediction_prob')
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image = self.rnn_wrapper.plot2image(buffer, 0)
        self.rnn_wrapper.add_image2board(name, image)
        plt.cla()
        plt.clf()
        plt.close('all')

