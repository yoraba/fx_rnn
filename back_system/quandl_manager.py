import quandl
import pandas as pd
from .shared import SharedLogic
from .constants import Constants
from .data.indicative_document import IndicativeDocument


class QuandlManager:

    def get_history(self, code, start_date=""):
        if start_date == "":
            start_date = SharedLogic.Config.General.start_date
        df = quandl.get(code, authtoken=SharedLogic.Config.Encrypted.quandl_token, start_date=start_date)
        return df

    def set_indicative_history(self):
        merged = pd.DataFrame()
        for item in Constants.QC_INDICATIVE.items():
            response: pd.DataFrame = self.get_history(item[1])
            response = response.rename(columns={'Value': item[0]})
            if merged.empty:
                merged = response
                continue
            merged = merged.merge(response, on='Date')
        IndicativeDocument.drop_collection()
        for doc in IndicativeDocument().df2doc_gen(merged):
            doc.save()

    def get_indicative_histoty(self):
        return IndicativeDocument().docs2df()







