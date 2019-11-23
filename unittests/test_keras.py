import unittest
import pandas as pd
import numpy as np
from mylib.logic.talib_wrapper import TAlibWrapper
from mylib.ai.keras_wrapper import RNNWrapper, RNNContext
from .aop_unittest import AOPUnitTest
from pandas import plotting


class RNNTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._path = './unittests/dat/USDJPY1440.csv'
        cls.load_csv()
        rnn_context = RNNContext()
        rnn_context.model_dir = './unittests/dat/model'
        rnn_context.model_name = 'rnn_model.json'
        rnn_context.weight_name = 'rnn_weight.hdf5'
        rnn_context.tensor_board_dir = './unittests/dat/tensorboard'
        cls.rnn_wrapper = RNNWrapper(rnn_context)

    @classmethod
    def load_csv(cls):
        cls._data = pd.read_csv(cls._path, index_col=0, parse_dates=True)
        cls._data = cls._data.sort_index(0, ascending=True)
        # print(cls._data.columns.values)
        cls._data = np.array(cls._data.loc[:, 'Open'], dtype='f8')
        # print(cls._data)

    @AOPUnitTest()
    def test_preprocess(self):
        answer = TAlibWrapper().get_technicals_of_series(self._data)
        before = np.shape(answer)
        answer = self.rnn_wrapper.preprocess(answer)
        answer = TAlibWrapper().add_high_low_data(answer)
        after = np.shape(answer)
        print(before, after)
        # self.assertEqual(before, after)
        # print(answer)
        print(f'min={np.min(answer)} max={np.max(answer)}')
        self.assertTrue(np.round(np.min(answer), 5) >= 0.)
        self.assertTrue(np.round(np.max(answer), 5) <= 1.)
        frame = pd.DataFrame(answer).iloc[:, :5]
        print(np.shape(frame))
        plotting.scatter_matrix(frame)
        import matplotlib.pyplot as plt
        plt.show()
        return True

    @AOPUnitTest()
    def test_make_data_and_label(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        X, y = self.rnn_wrapper.make_data_and_label(pre)
        print(np.shape(X), np.shape(y))
        return True

    @AOPUnitTest()
    def test_test_sprit(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        partition = round(len(pre)*0.7)
        Xtrain, ytrain = Xall[:partition], yall[:partition]
        print(np.shape(Xall), np.shape(yall), np.shape(Xtrain), np.shape(ytrain))
        self.assertEqual(partition, len(Xtrain))

    @AOPUnitTest()
    def test_create_model(self):
        print(self.rnn_wrapper.create_basic_lstm_model([[[1]]]))

    @AOPUnitTest()
    def test_fit(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        partition = round(len(pre) * 0.7)
        Xtrain, ytrain = Xall[:partition], yall[:partition]
        model = self.rnn_wrapper.create_basic_lstm_model(Xtrain)
        result = self.rnn_wrapper.fit(model, Xtrain, ytrain)
        self.rnn_wrapper.save2file(result)

    @AOPUnitTest()
    def test_predict(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        model = self.rnn_wrapper.loadModelFfile()
        prediction = model.predict(Xall)
        import matplotlib.pyplot as plt
        x = range(len(yall))
        y = yall[:, 5]
        pred_y = prediction[:, 5]
        plt.ylim(-0.1, 1.1)
        plt.plot(x, [0.5]*len(y), label='border')
        plt.plot(x, y, label='answer')
        plt.plot(x, pred_y, label='prediction_prob')
        plt.plot(x, yall[:, 0], label='price')
        plt.legend()
        plt.show()

    @AOPUnitTest()
    def test_high_low_price(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        model = self.rnn_wrapper.loadModelFfile()
        prediction = model.predict(Xall)
        match = self.rnn_wrapper.high_low_score(yall, prediction)
        print(f"{match} / {len(yall)}")

    @AOPUnitTest()
    def test_high_low_probability(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        model = self.rnn_wrapper.loadModelFfile()
        prediction = model.predict(Xall)
        match = self.rnn_wrapper.high_low_probability_score(yall, prediction, 5)
        print(f"{match} / {len(yall)} {match/len(yall)}%")

    @AOPUnitTest()
    def test_rmse(self):
        technical = TAlibWrapper().get_technicals_of_series(self._data)
        pre = self.rnn_wrapper.preprocess(technical)
        pre = TAlibWrapper().add_high_low_data(pre)
        Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
        partition = round(len(pre) * 0.7)
        Xtrain, ytrain = Xall[:partition], yall[:partition]
        Xtest, ytest = Xall[partition:], yall[partition:]
        model = self.rnn_wrapper.loadModelFfile()
        rmse_train, rmse_test = self.rnn_wrapper.rmse_score(model, Xtrain, Xtest, ytrain, ytest, 0)
        print(f"RMSE train: {rmse_train} RMSE test: {rmse_test}")

    # @AOPUnitTest()
    # def test_evaluate(self):
    #     technical = TAlibWrapper().get_technicals_of_series(self._data)
    #     pre = self.rnn_wrapper.preprocess(technical)
    #     pre = TAlibWrapper().add_high_low_data(pre)
    #     Xall, yall = self.rnn_wrapper.make_data_and_label(pre)
    #     partition = round(len(pre) * 0.7)
    #     Xtest, ytest = Xall[partition:], yall[partition:]
    #     model = self.rnn_wrapper.loadModelFfile()
    #     score = model.evaluate(Xtest, ytest, verbose=0)
    #     print(f"Test loss: {score[0]} Test accuracy: {score[1]}")
if __name__ == '__main__':
    unittest.main()