import datetime
import schedule
import time

from connector.auth_stack import AuthStack
from inference.symbol_factory import SymbolFactory


def get_symbols():
    return [{"symbol": "icici"}]


if __name__ == "__main__":
    # todo : need to be handled by a pipeline object for futher testability
    symbol_factory = SymbolFactory(get_symbols(),AuthStack())
    i = 0
    for symbol in symbol_factory.symbols:
        schedule.every(1).minutes.do(symbol.symbol_action)
        # schedule to morning 9:30 and separate each symbol by a lapse of a second
        schedule.jobs[-1].next_run = datetime.datetime.now().replace(hour=9, minute=30, second=i)
        i += 15

    # look for any new tasks if they are there
    while 1:
        schedule.run_pending()
        # for now 15 seconds is good but ideally this should be decided by the number of lapses in time gap
        time.sleep(15)
