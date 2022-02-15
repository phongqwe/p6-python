from abc import ABC


class ToJsonStr(ABC):
    """can convert itself into a json string"""
    def toJsonStr(self)->str:
        """convert itself into a json string"""
        raise NotImplementedError()