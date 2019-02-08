import pickle
import munch
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import talib as ta

class Symbol(object):
    def __init__(self, symbol, configurator):
        self.symbol = munch.munchify(symbol)
        self.configurator = configurator
        with open(self.symbol.model_path, 'rb') as file:
            self.model=pickle.load(file)
        self.data = self.load_daily_data()

    def symbol_action(self):
        new_data = self.get_new_data()
        signal = "No updates in data"
        if new_data.shape[0]>0:
            new_data.date=new_data.date.apply(lambda a:a.replace(tzinfo=None))
            self.data=self.data.append(new_data,ignore_index=False)
            self.data=self.data.iloc[1:]
            signal=self.predict_market(self.data)

        print("last data imput: %s" % str(self.data.iloc[-1].to_string()))
        print("got a signal %s" % signal)
        print("current time : %s \n" % str(datetime.now()))

    def get_new_data(self):
        from_time=list(self.data.date)[-1]
        to_time=datetime.today()
        new_data=self.configurator.kite.historical_data(instrument_token=self.instrument_token,
                                                        from_date=from_time,to_date=to_time,
                                                        interval=self.symbol.interval, continuous=0)
        new_data=pd.DataFrame(new_data)
        return new_data

    def load_daily_data(self):
        trade_ce=False
        trade_pe=False
        order_id=None
        NFO_data= self.configurator.kite.instruments("NFO")
        fut_s={}
        contract={}
        for i in range(len(NFO_data)):
            if (NFO_data[i]["tradingsymbol"].startswith(self.symbol.symbol_name)) and (NFO_data[i]['instrument_type']=='FUT') :
                fut_s[NFO_data[i]["expiry"]]=NFO_data[i]["instrument_token"]
                self.instrument_token=fut_s[min(fut_s.keys())]
                if min(fut_s.keys())==NFO_data[i]["expiry"]:
                    contract=NFO_data[i]
        from_date=(datetime.now() - timedelta(days=1))
        to_date=datetime.today()
        df=self.configurator.kite.historical_data(instrument_token=self.instrument_token,
                                from_date=from_date,to_date=to_date,
                                interval=self.symbol.interval, continuous=0)
        df=pd.DataFrame(df)
        df.date=df.date.apply(lambda a:a.replace(tzinfo=None))
        #df.set_index('date',inplace=True)
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

        X=self.create_features(df)
        min_len=(len(df)-len(X))+1
        df=df.iloc[-min_len:]
        return df

    def create_features(self,data):
        # Returns
        data=data.copy()
        col1=set(data.columns)
        data.set_index(data.date,inplace=True)
        data['Hour']=data.index.hour
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

    def predict_market(self,data):
        X=self.create_features(data)
        cls=self.model
        predictions= cls.predict(X)
        return predictions[-1]
