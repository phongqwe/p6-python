from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition
from com.github.xadkile.bicp.doc.data_structure.cell_container.CellContainer import CellContainer
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range


class SheetImp(CellContainer):
    """
    Sheet is a dict or Col objects
    """
    def cell(self,cellPos:CellPosition)->Cell:
        # return self.__colDict[cellPos.getColIndex()].getCell(cellPos)
        # this should evaluate the content of the cell
        pass

    # TODO this sign has wrong input arg
    def range(self,colIndex:int, rowIndex:int)->Range:
        pass

    def col(self,colIndex:int)->Range:
        """:return a column at an index"""
        pass

    def row(self,rowIndex:int)->Range:
        """:return a row at an index"""
        pass
