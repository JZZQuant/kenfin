from weakref import WeakValueDictionary


class Singleton(type):
    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AuthSingletonStack(metaclass=Singleton):
    def __init__(self):
        self.__keys__ = [
            {'api_key': "zka582z590jag8yh", 'secret_key': "9zdlmklim6rsakd2fkhay59hybsm5mw6", 'u_id': "RD0291",
             'password': "Divakar@1983"}]

    def pop(self):
        return self.__keys__.pop()

    def is_empty(self):
        return len(self.__keys__) == 0


class TestAuthSingletonStack(AuthSingletonStack):
    def __init__(self):
        self.__keys__ = [1, 2, 4, 5]


