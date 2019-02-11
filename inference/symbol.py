import pickle

import kiteconnect
import munch
from datetime import datetime, timedelta
import time
import pandas as pd
from logger.heirarchical_logger import info, debug, error


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
        if new_data.shape[0] > 0:
            new_data.date = new_data.date.apply(lambda a: a.replace(tzinfo=None))
            valid_new_entries = len(set(new_data.date).difference(set(self.data.date)))
            if valid_new_entries > 0:
                self.data = self.data.append(new_data, ignore_index=False)
                self.data = self.data.iloc[valid_new_entries:]
                if self.current_open is None:
                    self.current_open = self.data.iloc[-valid_new_entries]
                signal = self.predict_market()

        if signal is None:
            info("No valid updates to data")
        else:
            info("got a signal: %s" % signal)
        debug("last data input: \n%s" % str(self.data.iloc[-1].to_string()))

    def get_new_data(self):
        from_time = list(self.data.date)[-1]
        to_time = datetime.now()
        return self.get_all_data(from_time, to_time, self.instrument_token)

    def get_all_data(self, from_time, to_time, token):
        try:
            return pd.DataFrame(self.configurator.kite.historical_data(instrument_token=token,
                                                                       from_date=from_time, to_date=to_time,
                                                                       interval=self.symbol.interval, continuous=0))
        except kiteconnect.exceptions.NetworkException as e:
            error(e)
            return pd.DataFrame()

    def load_daily_data(self):
        symbol_trades = [nfo for nfo in self.configurator.nfo if
                         (nfo["tradingsymbol"].startswith(self.symbol.symbol_name)) and (
                                 nfo['instrument_type'] == self.symbol.instrument_type)]
        contract = sorted(symbol_trades, key=lambda x: x["expiry"])[0]
        from_date = datetime.now() - timedelta(days=1)
        to_date = datetime.today()
        yesterdays_data = self.get_all_data(from_date, to_date, contract["instrument_token"])
        while not yesterdays_data.shape[0]:
            yesterdays_data = self.get_all_data(from_date, to_date, contract["instrument_token"])
            time.sleep(10)

        yesterdays_data.date = yesterdays_data.date.apply(lambda a: a.replace(tzinfo=None))
        X = self.symbol.transformation(yesterdays_data)
        min_len = (len(yesterdays_data) - len(X)) + 10  # adding more data to handle duplicates
        df = yesterdays_data.iloc[-min_len:]
        return df, contract["instrument_token"]

    def predict_market(self):
        X = self.symbol.transformation(self.data)
        return self.model.predict(X)[-1]
