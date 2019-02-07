# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 20:31:04 2019

@author: udish
"""

import pandas as pd
import talib as ta
from load_model import load_model
import pickle
import get_data_first_time as g

with open("z.pkl",'rb') as z:
    kite=pickle.load(z)
def create_features(data):
    
    # Returns
    data=data.copy()
    col1=set(data.columns)
    data.date=data.date.map( lambda z:z.replace('+05:30',''))
    data.date=pd.to_datetime(data.date)
    data.set_index(data.date,inplace=True)
    data['Hour']=data.index.hour
#    data['Minute']=data.index.minute
    data['ret1'] = data.close.pct_change()
    data['ret2'] = data.close.pct_change(2)
    data['ret5'] = data.close.pct_change(5)
    data['ret20'] = data.close.pct_change(20)
    data['ret30'] = data.close.pct_change(30)

    data['retl1'] = data.low.pct_change()
    data['retl2'] = data.low.pct_change(2)
    data['retl5'] = data.low.pct_change(5)
    data['reth1'] = data.high.pct_change()
    data['reth2'] = data.high.pct_change(2)
    data['reth5'] = data.high.pct_change(5)
    
    
    data['retr5'] = data.ret1.rolling(5).sum() 
    data['retr10'] = data.ret1.rolling(10).sum()
    data['retr20'] = data.ret1.rolling(20).sum()
    data['retr40'] = data.ret1.rolling(40).sum()

    # Standard Deviation
    data['std5'] = data.ret1.rolling(5).std()
    data['std10'] = data.ret1.rolling(10).std()
    data['std20'] = data.ret1.rolling(20).std()
    data['std40'] = data.ret1.rolling(30).std()


    data['vel1'] = (2*data.close-data.high-data.low)
    data['vel5'] = data.vel1.rolling(5).sum()
    data['vel10'] = data.vel1.rolling(10).sum()
    data['vel20'] = data.vel1.rolling(20).sum()
    data['vel40'] = data.vel1.rolling(30).sum()
    
    data['stdv5'] = data.vel1.rolling(5).std()
    data['stdv10'] = data.vel1.rolling(10).std()
    data['stdv20'] = data.vel1.rolling(20).std()
    data['stdv40'] = data.vel1.rolling(30).std()
    
    
    data['stdv5'] = data.volume.rolling(5).std()
    data['stdvv10'] = data.volume.rolling(10).std()
    data['stdvv20'] = data.volume.rolling(20).std()
    data['stdvv40'] = data.volume.rolling(30).std()
    
        
    # ADDED volume profile and acc, this reduced low vol peformance but increased the high vol performance
 
    data['vol1'] = data.volume.diff()
    data['vol5'] = data.volume.diff(5)
    data['vol10'] = data.volume.diff(10)
    data['vol20'] = data.volume.diff(20)
    data['vol40'] = data.volume.diff(30)
    
    data['vols5'] = data.volume.rolling(5).sum()
    data['vols10'] = data.volume.rolling(10).sum()
    data['vols20'] = data.volume.rolling(20).sum()
    data['vols40'] = data.volume.rolling(30).sum()
    
    data['acc1'] = data.vel1.diff()
    data['acc5'] = data.vel1.diff(5)
    data['acc10'] = data.vel1.diff(10)
    data['acc20'] = data.vel1.diff(20)
    data['acc40'] = data.vel1.diff(30)
     
    # Candlestick Patterns
    data['HAMMER']=ta.CDLHAMMER(data.open, data.high, data.low, data.close)
    data['DOJI']=ta.CDLDOJI(data.open, data.high, data.low, data.close)
    data['SHOOTINGSTAR']=ta.CDLSHOOTINGSTAR(data.open, data.high, data.low, data.close)
    
    # Technical Indicators
    
# changed the timeperiod from 14 to 30
    data['AROONOSC']=ta.AROONOSC( data.high, data.low ,timeperiod=30)
    data['AROONOSC10']=ta.AROONOSC( data.high, data.low ,timeperiod=10)
    data['AROONOSC20']=ta.AROONOSC( data.high, data.low ,timeperiod=20)
    data['AROONOSC5']=ta.AROONOSC( data.high, data.low ,timeperiod=5)

    data['RSI']=ta.RSI(data.close,timeperiod=30)
    data['RSI14']=ta.RSI(data.close,timeperiod=14)
    data['RSI10']=ta.RSI(data.close,timeperiod=10)

    data['ADXR']=ta.ADXR(  data.high, data.low, data.close,timeperiod=30)    
    data['ADXR']=ta.ADXR(  data.high, data.low, data.close,timeperiod=15)    

    
    data['ATR30']=ta.ATR(data.high,data.low,data.close,timeperiod=30)
    data['ATR']=ta.ATR(data.high,data.low,data.close,timeperiod=5)
    data['ATR10']=ta.ATR(data.high,data.low,data.close,timeperiod=10)
    data['ATR20']=ta.ATR(data.high,data.low,data.close,timeperiod=20)    
# Adding jump
    data['Jump']=data.open-data.close.shift(1)
    data['Jump5']=data.open-data.close.shift(5)
    data['Jump10']=data.open-data.close.shift(10)
    data['Jump20']=data.open-data.close.shift(20)
    data['Jump30']=data.open-data.close.shift(30)


    col2=set(data.columns)

    # Define predictor variables (X) and a target variable (y)
    data = data.dropna()
    predictor_list = list(col2-col1)
    X = data[predictor_list]

    return X 
def predict_market(data,model_saved_name):
    # Create feature from the raw data
    X=create_features(data)
    model=load_model(model_saved_name)
    cls=model.best_estimator_
    predictions= cls.predict(X)
    return predictions[-1]
# You need to provide the name for the model that you us eon your lcoal machine
signal=predict_market(g.df,model_saved_name)

if signal==1:
    g.trade_ce=True
    g.trade_pe=False

elif signal==-1:
    g.trade_pe=True
    g.trade_ce=False

# Need to work on the exit
if g.trade_ce==True:
    if g.order_id==None:
        g.order_id=kite.place_order(tradingsymbol=g.options_ce,quantity =g.contract['lot_size'], 
                              order_type="LIMIT",exchange="NSE",price=g.df.close.iloc[-1],
                              transaction_type="BUY",product="MIS")

        
if g.trade_pe==True:
    if g.order_id==None:
        g.order_id=kite.order_place(tradingsymbol=g.options_pe,quantity =g.contract['lot_size'], 
                              order_type="LIMIT",exchange="NSE",price=g.df.close.iloc[-1],
                              transaction_type="BUY",product="MIS")