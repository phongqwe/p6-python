from bicp_document_structure.cell.cache.DataCache import DataCache


class DataCacheImp(DataCache):

    def __init__(self, value=None):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):
        """ set the cached value """
        self.__value = newValue