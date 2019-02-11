from etl.transformations import *

def tradables():
    return [{"symbol_name": "ICICI", "interval": "minute", "model_path": "../resources/pkls/icici.pkl","instrument_type":"FUT" , "transformation" : icic_fut_transform }]
