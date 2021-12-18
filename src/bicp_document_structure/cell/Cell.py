from bicp_document_structure.cell.address.CellAddress import CellAddress


class Cell:
    """
    Cell interface
    """
    @property
    def value(self):
        pass

    @value.setter
    def value(self,newValue):
        pass

    @property
    def code(self)->str:
        pass

    @code.setter
    def code(self,newCode:str):
        pass

    @property
    def address(self)->CellAddress:
        pass

    @property
    def row(self) -> int:
        return self.address.rowIndex

    @property
    def col(self) -> int:
        return self.address.colIndex

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

    def runCode(self, globalScope=None, localScope=None):
        pass