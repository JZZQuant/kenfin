# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 21:01:49 2019

@author: udish
"""

import pickle
from datetime import datetime, timedelta
from predict_market import create_features
import pandas as pd
import numpy as np
stock='ICICI'
interval="minute"
trade_ce=False
trade_pe=False
order_id=None
with open("z.pkl",'rb') as z:
    kite=pickle.load(z)

NFO_data= kite.instruments("NFO")
fut_s={}
contract={}
for i in range(len(NFO_data)):
    if((NFO_data[i]["tradingsymbol"].startswith(stock))&
        (NFO_data[i]['instrument_type']=='FUT')):
        fut_s[NFO_data[i]["expiry"]]=NFO_data[i]["instrument_token"]
        instrument_token=fut_s[min(fut_s.keys())]
        if instrument_token==NFO_data[i]["expiry"]:
            contract=NFO_data[i]
    from_date=(datetime.now() - timedelta(days=1))
    to_date=datetime.today()
    df=kite.historical_data(instrument_token=instrument_token,
                            from_date=from_date,to_date=to_date,
                            interval=interval, continuous=0)
    df=pd.DataFrame(df)
    df.date=df.date.apply(lambda a:a.replace(tzinfo=None))
    df.set_index('date',inplace=True)
    closes=df.iloc[-1].close
    
opt_s={}
for i in range(len(NFO_data)):
    if((NFO_data[i]["tradingsymbol"].startswith("ICICI"))&
        (NFO_data[i]['instrument_type']=='CE')):
        opt_s[NFO_data[i]["instrument_token"]]=NFO_data[i]["strike"]
strikes=list(opt_s.values())
loc=np.argmin(np.absolute(strikes-closes))
strike=strikes[loc]
symbol=contract['tradingsymbol']
options_ce=symbol[:-3]+str(int(strike))+'CE'
options_pe=symbol[:-3]+str(int(strike))+'PE'

X=create_features(df)
min_len=(len(df)-len(X))+1
df=df.iloc[-min_len:]
