from abc import ABC


class ToException(ABC):
    """ able to produce an exception """
    def toException(self)->Exception:
        return Exception(str(self))