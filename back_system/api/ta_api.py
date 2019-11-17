import numpy as np
from mylib.logic.talib_wrapper import TAlibWrapper
from back_system.data.indicative_document import IndicativeDocument


class TAlib_API:

    def __init__(self, context):
        self.context = context
        self.wrapper = TAlibWrapper()

    def get_technicals(self):
        df =IndicativeDocument().docs2df()
        result = None
        for idx1, item in enumerate(df.columns.values[1:]):
            answer = self.wrapper.get_technicals_of_series(df.loc[:, item])
            if result is None:
                result = answer
            else:
                result = np.hstack((result, answer))
        # print(np.shape(result))
        return result

