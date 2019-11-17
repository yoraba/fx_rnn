import quandl
import pandas as pd
from back_system.shared import SharedContext
from back_system.constants import Constants
from back_system.data.indicative_document import IndicativeDocument


class QuandlAPI:

    def __init__(self, context: SharedContext):
        self.context: SharedContext = context

    def get_history_from_quandl(self, code, start_date=""):
        if start_date == "":
            start_date = self.context.Config.General.start_date
        df = quandl.get(code, authtoken=self.context.Config.Encrypted.quandl_token, start_date=start_date)
        return df

    def set_indicative_history(self):
        merged = pd.DataFrame()
        for item in Constants.QC_INDICATIVE.items():
            response: pd.DataFrame = self.get_history_from_quandl(item[1])
            response = response.rename(columns={'Value': item[0]})
            if merged.empty:
                merged = response
                continue
            merged = merged.merge(response, on='Date')
        IndicativeDocument.drop_collection()
        for doc in IndicativeDocument().df2doc_gen(merged):
            doc.save()

    def get_indicative_history_df(self):
        return IndicativeDocument().docs2df()

    def get_indicative_history_dict(self):
        return IndicativeDocument().docs2dict()

