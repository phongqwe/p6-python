from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.cache.DataCache import DataCache
from bicp_document_structure.cell.cache.DataCacheImp import DataCacheImp


class CacheCell(Cell):
    """
    A decorator that add a cache functionality to a Cell. A cache cell only execute code if the internal cache object is empty
    """
    def __init__(self,cell:Cell,cache:DataCache = None):
        self.__cell:Cell = cell
        if cache is None:
            cache = DataCacheImp()
        self.__cache:DataCache = cache

    @property
    def displayValue(self) -> str:
        return self.__cell.displayValue

    def bareValue(self):
        return self.__cell.bareValue()

    @property
    def value(self):
        if self.__cache.isNotEmpty():
            return self.__cache.value
        else:
            v = self.__cell.value
            self.__cache.value = v
            return v

    @property
    def script(self) -> str:
        return self.__cell.script

    @property
    def address(self) -> CellAddress:
        return self.__cell.address

    def runScript(self, globalScope=None, localScope=None):
        return self.__cell.runScript(globalScope, localScope)

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
        self.__cache.clear()
        self.__cell.setScriptAndRun(newScript, globalScope, localScope)
        self.__cache.value = self.bareValue()

    def hasCode(self) -> bool:
        return self.__cell.hasCode()

    def toJson(self) -> CellJson:
        return self.__cell.toJson()