from connector.configurator import Configurator
from itertools import cycle
from inference.symbol import Symbol


class SymbolFactory(object):
    def __init__(self, symbols, auth_singleton_stack):
        self.configs = auth_singleton_stack
        self.executors = cycle(self.__get_executors__())
        self.symbols = self.__map_executors__(symbols)

    def __get_executors__(self):
        while not self.configs.is_empty():
            yield Configurator()

    def __map_executors__(self, symbols):
        for symbol in symbols:
            yield Symbol(symbol, next(self.executors))


class TestSymbolFactory(SymbolFactory):
    def __get_executors__(self):
        while not self.configs.is_empty():
            yield self.configs.pop()

