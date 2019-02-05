class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AuthStack(metaclass=Singleton):
    def __init__(self):
        # in an ideal scenario these will come from a database
        self.__keys__ = [
            {'api_key': "zka582z590jag8yh", 'secret_key': "9zdlmklim6rsakd2fkhay59hybsm5mw6", 'u_id': "RD0291",
             'password': "Divakar@1983"}]

    def pop(self):
        return self.__keys__.pop()

    def is_empty(self):
        return len(self.__keys__) == 0