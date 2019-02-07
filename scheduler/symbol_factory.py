from connector.auth_stack import *
from connector.configurator import Configurator
from itertools import cycle
from scheduler.symbol import Symbol


class SymbolFactory(object):
    def __init__(self, symbols):
        self.configs = AuthStack()
        self.executors = cycle(self.__get_executors__())
        self.symbols = self.__map_executors__(symbols)

    def __get_executors__(self):
        while not self.configs.is_empty():
            yield Configurator()

    def __map_executors__(self, symbols):
        for symbol in symbols:
            yield Symbol(symbol, next(self.executors))


# todo : need to make it testable
class TestSymbolFactory(object):
    def __init__(self, symbols):
        self.configs = TestAuthStack()
        self.executors = cycle(self.__get_executors__())
        self.symbols = self.__map_executors__(symbols)

    def __get_executors__(self):
        while not self.configs.is_empty():
            yield self.configs.pop()

    def __map_executors__(self, symbols):
        for symbol in symbols:
            yield Symbol(symbol, next(self.executors))
