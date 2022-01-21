from abc import ABC


class DataCache(ABC):
    def clear(self):
        """ delete the cached value"""
        self.value = None

    def isNotEmpty(self):
        """return true if cached value is not none"""
        return self.value is not None

    def isEmpty(self):
        return self.value is None

    @property
    def value(self):
        """ get the cached value """
        raise NotImplementedError()

    @value.setter
    def value(self,newValue):
        """ set the cached value """
        raise NotImplementedError()