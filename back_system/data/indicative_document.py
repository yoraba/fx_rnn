from mongoengine.document import Document
from mongoengine import fields
from mylib.db.mongoengine_wrapper import *


class IndicativeDocument(DocumentWrapper):
    Date = fields.DateTimeField(required=True)
    USDJPY = fields.FloatField()
    EURJPY = fields.FloatField()
    GBPJPY = fields.FloatField()
    EURUSD = fields.FloatField()
    GBPUSD = fields.FloatField()
    NZDUSD = fields.FloatField()
    EURGBP = fields.FloatField()
