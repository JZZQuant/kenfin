from connector.auth_stack import AuthSingletonStack
from connector.configurator import Configurator
from itertools import cycle
from inference.symbol import Symbol
import settings


class SymbolFactory(object):
    def __init__(self, symbols):
        self.executors = cycle(self.__get_executors__())
        self.symbols = [Symbol(symbol, next(self.executors)) for symbol in symbols]

    def __get_executors__(self):
        while not AuthSingletonStack.is_empty():
            if settings.chrome_driver_path is not None:
                yield Configurator(settings.chrome_driver_path)
            else :
                yield Configurator()


class TestSymbolFactory(SymbolFactory):
    def __get_executors__(self):
        while not AuthSingletonStack.is_empty():
            yield AuthSingletonStack.pop()
