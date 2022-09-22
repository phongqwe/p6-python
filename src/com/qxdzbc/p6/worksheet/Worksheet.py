from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union, Tuple

from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell_container.MutableCellContainer import MutableCellContainer
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.worksheet.rpc_data_structure import WorksheetId
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto
from com.qxdzbc.p6.worksheet.LoadType import LoadType

if TYPE_CHECKING:
    from com.qxdzbc.p6.range.Range import Range


class Worksheet(MutableCellContainer,
                ToProto[WorksheetProto],
                ABC):

    def updateMultipleCellRs(self,updateEntries:[IndCell])->Result[None, ErrorReport]:
        raise NotImplementedError()

    def updateMultipleCell(self,updateEntries:list[IndCell]):
        raise NotImplementedError()

    @property
    def id(self) -> WorksheetId:
        raise NotImplementedError()

    def load2DArrayRs(
            self, data2DArray,
            anchorCell: CellAddress= CellAddresses.A1,
            loadType: LoadType=LoadType.KEEP_OLD_DATA_IF_COLLIDE
    ) -> Result['Worksheet', ErrorReport]:
        """
        :param data2DArray: a python array or anything that is array-like
        :param anchorCell: starting point to load the data into
        :param loadType: load type
        :return: a Result obj encasing a new worksheet with the loaded data, but in case or a rpc worksheet (which is stateless), that is just the old worksheet.
        """
        raise NotImplementedError()

    def load2DArray(
            self, dataAray,
            anchorCell: CellAddress= CellAddresses.A1,
            loadType: LoadType=LoadType.KEEP_OLD_DATA_IF_COLLIDE
    )-> 'Worksheet':
        """
        :param dataAray: a python array or anything that is array-like
        :param anchorCell: starting point to load the data into
        :param loadType: load type
        :return: a new worksheet with the loaded data, but in case or a rpc worksheet (which is stateless), that is just the old worksheet.
        :raise: an exception if there are errors.
        """
        raise NotImplementedError()

    def loadDataFrame(
            self, dataFrame,
            anchorCell: CellAddress= CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader: bool = True,
    ) -> 'Worksheet':
        """
        load a pandas data frame into this worksheet
        :param keepHeader: keep or not keep column header in the input pandas DataFrame
        :param anchorCell: a starting point to load the data
        :param dataFrame: a pandas dataframe
        :param loadType: controls how the data should be loaded (overwrite everything, keep old data, etc)
        :return: a new worksheet with the loaded data, but in case or a rpc worksheet (which is stateless), that is just the old worksheet.
         :raise: an exception if there are errors.
        """
        raise NotImplementedError()

    def loadDataFrameRs(
            self, dataFrame,
            anchorCell: CellAddress= CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader:bool=True,
    ) -> Result['Worksheet', ErrorReport]:
        """
        load a pandas data frame into this worksheet
        :param keepHeader: keep or not keep column header in the input pandas DataFrame
        :param anchorCell: a starting point to load the data
        :param dataFrame: a pandas dataframe
        :param loadType: controls how the data should be loaded (overwrite everything, keep old data, etc)
       :return: a Result obj encasing a new worksheet with the loaded data, but in case or a rpc worksheet (which is stateless), that is just the old worksheet.
        """
        raise NotImplementedError()

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        raise NotImplementedError()

    @property
    def wbKey(self) -> WorkbookKey:
        raise NotImplementedError()

    @property
    def maxUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def maxUsedRow(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedRow(self) -> int | None:
        raise NotImplementedError()

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        raise NotImplementedError()

    @property
    def usedRange(self) -> Range | None:
        raise NotImplementedError()

    def pasteRs(self, cell: CellAddress) -> Result[None, ErrorReport]:
        """paste what inside the system clipboard into the sheet, starting at a cell"""
        raise NotImplementedError()

    def paste(self, cell: CellAddress):
        raise NotImplementedError()

    def compareContent(self, ws2: Worksheet) -> bool:
        """Compare equality by comparing name and comparing all cell of this sheet with another. Very inefficient, use with care"""
        raise NotImplementedError()

    @property
    def cellCount(self):
        raise NotImplementedError()

    @property
    def rootWorksheet(self) -> 'Worksheet':
        """the root worksheet is the lowest layer (data layer) worksheet, not hooked to any event callbacks, not wrapped in any wrapper. For data-layer worksheet, this is itself. For wrapper worksheet, this is their inner worksheet"""
        raise NotImplementedError()

    def toProtoObj(self) -> WorksheetProto:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    def rename(self, newName: str):
        raise NotImplementedError()

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        raise NotImplementedError()
