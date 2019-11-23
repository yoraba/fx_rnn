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
        self.fit()
        model = self.rnn_wrapper.loadModelFfile()
        (Xall, yall, Xtrain, ytrain, Xtest, ytest) = self.create_data()
        prediction = model.predict(Xall)
        high_row_score = []
        for i in range(np.shape(yall)[1]):
            match = self.rnn_wrapper.high_low_probability_score(yall, prediction, i)
            high_row_score.append(match / len(yall))
        return high_row_score

