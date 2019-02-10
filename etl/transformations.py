import pandas as pd
import talib as ta

def icic_fut_transform(self, data):
    data.drop_duplicates(subset='date', keep="first", inplace=True)
    feature_frame = pd.DataFrame()
    feature_frame['Hour'] = data['date'].apply(lambda x: x.hour)
    feature_frame['ret1'] = data.close.pct_change()
    feature_frame['ret2'] = data.close.pct_change(2)
    feature_frame['ret5'] = data.close.pct_change(5)
    feature_frame['ret20'] = data.close.pct_change(20)
    feature_frame['ret30'] = data.close.pct_change(30)

    feature_frame['retl1'] = data.low.pct_change()
    feature_frame['retl2'] = data.low.pct_change(2)
    feature_frame['retl5'] = data.low.pct_change(5)
    feature_frame['reth1'] = data.high.pct_change()
    feature_frame['reth2'] = data.high.pct_change(2)
    feature_frame['reth5'] = data.high.pct_change(5)

    feature_frame['retr5'] = feature_frame.ret1.rolling(5).sum()
    feature_frame['retr10'] = feature_frame.ret1.rolling(10).sum()
    feature_frame['retr20'] = feature_frame.ret1.rolling(20).sum()
    feature_frame['retr40'] = feature_frame.ret1.rolling(40).sum()

    # Standard Deviation
    feature_frame['std5'] = feature_frame.ret1.rolling(5).std()
    feature_frame['std10'] = feature_frame.ret1.rolling(10).std()
    feature_frame['std20'] = feature_frame.ret1.rolling(20).std()
    feature_frame['std40'] = feature_frame.ret1.rolling(30).std()

    feature_frame['vel1'] = (2 * data.close - data.high - data.low)
    feature_frame['vel5'] = feature_frame.vel1.rolling(5).sum()
    feature_frame['vel10'] = feature_frame.vel1.rolling(10).sum()
    feature_frame['vel20'] = feature_frame.vel1.rolling(20).sum()
    feature_frame['vel40'] = feature_frame.vel1.rolling(30).sum()

    feature_frame['stdv5'] = feature_frame.vel1.rolling(5).std()
    feature_frame['stdv10'] = feature_frame.vel1.rolling(10).std()
    feature_frame['stdv20'] = feature_frame.vel1.rolling(20).std()
    feature_frame['stdv40'] = feature_frame.vel1.rolling(30).std()

    feature_frame['stdv5'] = data.volume.rolling(5).std()
    feature_frame['stdvv10'] = data.volume.rolling(10).std()
    feature_frame['stdvv20'] = data.volume.rolling(20).std()
    feature_frame['stdvv40'] = data.volume.rolling(30).std()

    # ADDED volume profile and acc, this reduced low vol peformance but increased the high vol performance

    feature_frame['vol1'] = data.volume.diff()
    feature_frame['vol5'] = data.volume.diff(5)
    feature_frame['vol10'] = data.volume.diff(10)
    feature_frame['vol20'] = data.volume.diff(20)
    feature_frame['vol40'] = data.volume.diff(30)

    feature_frame['vols5'] = data.volume.rolling(5).sum()
    feature_frame['vols10'] = data.volume.rolling(10).sum()
    feature_frame['vols20'] = data.volume.rolling(20).sum()
    feature_frame['vols40'] = data.volume.rolling(30).sum()

    feature_frame['acc1'] = feature_frame.vel1.diff()
    feature_frame['acc5'] = feature_frame.vel1.diff(5)
    feature_frame['acc10'] = feature_frame.vel1.diff(10)
    feature_frame['acc20'] = feature_frame.vel1.diff(20)
    feature_frame['acc40'] = feature_frame.vel1.diff(30)

    # Candlestick Patterns
    feature_frame['HAMMER'] = ta.CDLHAMMER(data.open, data.high, data.low, data.close)
    feature_frame['DOJI'] = ta.CDLDOJI(data.open, data.high, data.low, data.close)
    feature_frame['SHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(data.open, data.high, data.low, data.close)

    # changed the timeperiod from 14 to 30
    feature_frame['AROONOSC'] = ta.AROONOSC(data.high, data.low, timeperiod=30)
    feature_frame['AROONOSC10'] = ta.AROONOSC(data.high, data.low, timeperiod=10)
    feature_frame['AROONOSC20'] = ta.AROONOSC(data.high, data.low, timeperiod=20)
    feature_frame['AROONOSC5'] = ta.AROONOSC(data.high, data.low, timeperiod=5)

    feature_frame['RSI'] = ta.RSI(data.close, timeperiod=30)
    feature_frame['RSI14'] = ta.RSI(data.close, timeperiod=14)
    feature_frame['RSI10'] = ta.RSI(data.close, timeperiod=10)

    feature_frame['ADXR'] = ta.ADXR(data.high, data.low, data.close, timeperiod=30)
    feature_frame['ADXR'] = ta.ADXR(data.high, data.low, data.close, timeperiod=15)

    feature_frame['ATR30'] = ta.ATR(data.high, data.low, data.close, timeperiod=30)
    feature_frame['ATR'] = ta.ATR(data.high, data.low, data.close, timeperiod=5)
    feature_frame['ATR10'] = ta.ATR(data.high, data.low, data.close, timeperiod=10)
    feature_frame['ATR20'] = ta.ATR(data.high, data.low, data.close, timeperiod=20)
    # Adding jump
    feature_frame['Jump'] = data.open - data.close.shift(1)
    feature_frame['Jump5'] = data.open - data.close.shift(5)
    feature_frame['Jump10'] = data.open - data.close.shift(10)
    feature_frame['Jump20'] = data.open - data.close.shift(20)
    feature_frame['Jump30'] = data.open - data.close.shift(30)

    return feature_frame.dropna()
