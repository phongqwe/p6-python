from abc import ABC


class JsonStrMaker(ABC):
    def jsonStr(self)->str:
        raise NotImplementedError()