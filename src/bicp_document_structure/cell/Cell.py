from bicp_document_structure.cell.address.CellAddress import CellAddress


class Cell:
    """
    Cell interface
    """
    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self,newValue):
        raise NotImplementedError()

    @property
    def code(self)->str:
        raise NotImplementedError()

    @code.setter
    def code(self,newCode:str):
        raise NotImplementedError()

    @property
    def address(self)->CellAddress:
        raise NotImplementedError()

    @property
    def row(self) -> int:
        return self.address.rowIndex

    @property
    def col(self) -> int:
        return self.address.colIndex

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

    def runCode(self, globalScope, localScope):
        raise NotImplementedError()