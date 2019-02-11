from connector.auth_stack import AuthSingletonStack
from connector.configurator import Configurator
from itertools import cycle
from inference.symbol import Symbol


class SymbolFactory(object):
    def __init__(self, symbols):
        self.configs = AuthSingletonStack()
        self.executors = cycle(self.__get_executors__())
        self.symbols = [Symbol(symbol, next(self.executors)) for symbol in symbols]

    def __get_executors__(self):
        while not self.configs.is_empty():
            yield Configurator()


class TestSymbolFactory(SymbolFactory):
    def __get_executors__(self):
        while not self.configs.is_empty():
            yield self.configs.pop()
