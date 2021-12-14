from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition


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
    def pos(self)->CellPosition:
        pass

    @pos.setter
    def pos(self,newPos):
        pass

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value