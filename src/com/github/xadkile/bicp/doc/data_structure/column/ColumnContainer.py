from com.github.xadkile.bicp.doc.data_structure.column.Column import Column


class ColumnContainer:
    def hasColumn(self, colIndex: int) -> bool:
        """check if this holder has a column at an index"""
        pass

    def getCol(self, colIndex: int) -> Column:
        """get column at an index"""
        pass


class MutableColumnContainer(ColumnContainer):
    def setCol(self, index: int, col: Column):
        pass
