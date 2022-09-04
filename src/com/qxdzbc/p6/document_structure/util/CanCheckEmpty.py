from abc import ABC


class CanCheckEmpty(ABC):
    def isEmpty(self)->bool:
        raise NotImplementedError()
    def isNotEmpty(self)->bool:
        return not self.isEmpty()