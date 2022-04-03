import json
from abc import ABC


class ToJson(ABC):
    """can convert itself into a json string"""
    def toJsonStr(self)->str:
        """convert itself into a json string"""
        return json.dumps(self.toJsonDict())

    def toJsonDict(self)->dict:
        """convert itself into a json dict"""
        raise NotImplementedError()