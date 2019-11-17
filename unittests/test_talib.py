import unittest
import pandas as pd
import numpy as np
from mylib.logic.talib_wrapper import TAlibWrapper
from .aop_unittest import AOPUnitTest

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._path = './unittests/dat/USDJPY1440.csv'
        cls.load_csv()

    @classmethod
    def load_csv(cls):
        cls._data = pd.read_csv(cls._path, index_col=0, parse_dates=True)
        cls._data = cls._data.sort_index(0, ascending=True)
        # print(cls._data.columns.values)
        cls._data = np.array(cls._data.loc[:, 'Open'], dtype='f8')
        # print(cls._data)

    @AOPUnitTest()
    def test_technicals(self):
        answer = TAlibWrapper().get_technicals_of_series(self._data)
        print(answer)


if __name__ == '__main__':
    unittest.main()
