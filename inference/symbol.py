import pickle
import munch
from datetime import datetime, timedelta
import pandas as pd
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

class Symbol(object):
    def __init__(self, symbol, configurator):
        self.symbol = munch.munchify(symbol)
        self.configurator = configurator
        self.current_open = None
        with open(self.symbol.model_path, 'rb') as file:
            self.model = pickle.load(file)
        self.data, self.instrument_token = self.load_daily_data()
        self.prev_closing = self.data.iloc[-1]

    def symbol_action(self):
        new_data = self.get_new_data()
        # todo: looks clumsy needs a proper fix ,
        signal = None
        if new_data.shape[0] > 0 :
            new_data.date = new_data.date.apply(lambda a: a.replace(tzinfo=None))
            valid_new_entries = len(set(new_data.date).difference(set(self.data.date)))
            if valid_new_entries > 0:
                self.data = self.data.append(new_data, ignore_index=False)
                self.data = self.data.iloc[valid_new_entries:]
                if self.current_open is None :
                    self.current_open = self.data.iloc[-valid_new_entries]
                signal = self.predict_market()

        if signal is None:
            logging.info("No valid updates to data")
        else: logging.debug("got a signal %s" % signal)
        logging.info("last data imput: %s" % str(self.data.iloc[-1].to_string()))

    def get_new_data(self):
        from_time = list(self.data.date)[-1]
        to_time = datetime.today()
        return pd.DataFrame(self.configurator.kite.historical_data(instrument_token=self.instrument_token,
                                                                   from_date=from_time, to_date=to_time,
                                                                   interval=self.symbol.interval, continuous=0))

    def load_daily_data(self):
        symbol_trades = [nfo for nfo in self.configurator.nfo if
                         (nfo["tradingsymbol"].startswith(self.symbol.symbol_name)) and (
                                     nfo['instrument_type'] == self.symbol.instrument_type)]
        contract = sorted(symbol_trades, key=lambda x: x["expiry"])[0]
        from_date = datetime.now() - timedelta(days=1)
        to_date = datetime.today()
        df = pd.DataFrame(self.configurator.kite.historical_data(instrument_token=contract["instrument_token"],
                                                                 from_date=from_date, to_date=to_date,
                                                                 interval=self.symbol.interval, continuous=0))
        df.date = df.date.apply(lambda a: a.replace(tzinfo=None))
        X = self.symbol.transformation(df)
        min_len = (len(df) - len(X)) + 10 # adding more data to handle duplicates
        df = df.iloc[-min_len:]
        return df, contract["instrument_token"]

    def predict_market(self):
        X = self.symbol.transformation(self.data)
        return self.model.predict(X)[-1]
