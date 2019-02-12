import settings


class AuthSingletonStack:
    __keys__ = settings.keys()

    @staticmethod
    def pop():
        return AuthSingletonStack.__keys__.pop()

    @staticmethod
    def is_empty():
        return len(AuthSingletonStack.__keys__) == 0

    @staticmethod
    def __reset__():
        AuthSingletonStack.__keys__ = settings.keys()


class TestAuthSingletonStack(AuthSingletonStack):
    def __init__(self):
        self.__keys__ = [1, 2, 4, 5]
