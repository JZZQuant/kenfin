import datetime
import schedule
import time

from connector.auth_stack import AuthSingletonStack
from inference.symbol_factory import SymbolFactory


def get_tradables():
    return [{"symbol_name": "ICICI", "interval": "minute", "model_path": "../resources/pkls/icici.pkl","instrument_type":"FUT"}]

if __name__ == "__main__":
    # todo : need to be handled by a pipeline object for futher testability
    symbol_factory = SymbolFactory(get_tradables(), AuthSingletonStack())
    i = 0
    now=datetime.datetime.now()
    start = datetime.datetime.now().replace(hour=9, minute=30,second=0)
    close = datetime.datetime.now().replace(hour=15, minute=30,second=0)
    next_run = max(start,now)
    # if its post 3:30 schedule it for tomorrow
    if next_run > close:
        next_run = start+ datetime.timedelta(days=1)
    for symbol in symbol_factory.symbols:
        schedule.every(1).minutes.do(symbol.symbol_action)
        schedule.jobs[-1].next_run = next_run.replace(second=i)
        i += 15

    # look for any new tasks if they are there
    while datetime.datetime.now() < close:
        schedule.run_pending()
        time.sleep(1)
