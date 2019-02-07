# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 21:01:49 2019

@author: udish
"""

import pickle
from datetime import datetime
import pandas as pd
import get_data_first_time as g

with open("z.pkl",'rb') as z:
    kite=pickle.load(z)


from_time=g.df.iloc[-1].date
to_time=datetime.today()
new_data=kite.historical_data(instrument_token=g.instrument_token,
                            from_date=from_time,to_date=to_time,
                            interval=g.interval, continuous=0)
new_data=pd.DataFrame(new_data)
new_data.date=new_data.date.apply(lambda a:a.replace(tzinfo=None))
new_data.set_index('date',inplace=True)
g.df=g.df.append(new_data,ignore_index=True)
g.df=g.df.iloc[1:]
