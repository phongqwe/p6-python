from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union, Tuple

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

    @property
    def id(self) -> WorksheetId:
        raise NotImplementedError()

    def loadArrayRs(self, dataAray, anchorCell: CellAddress= CellAddresses.A1, loadType: LoadType=LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> Result['Worksheet', ErrorReport]:
        raise NotImplementedError()

    def loadArray(self, dataAray, anchorCell: CellAddress= CellAddresses.A1, loadType: LoadType=LoadType.KEEP_OLD_DATA_IF_COLLIDE)->'Worksheet':
        raise NotImplementedError()

    def loadDataFrame(self, dataFrame, anchorCell: CellAddress= CellAddresses.A1, loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> 'Worksheet':
        """
        load a pandas data frame into this worksheet
        :param dataFrame is a pandas dataframe
        :param loadType controls how the data should be loaded (overwrite everything, keep old data, etc)
        :return a worksheet containing the new data
        """
        raise NotImplementedError()

    def loadDataFrameRs(self, dataFrame, anchorCell: CellAddress= CellAddresses.A1, loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> Result['Worksheet', ErrorReport]:
        """
        load a pandas data frame into this worksheet
        :param dataFrame is a pandas dataframe
        :param loadType controls how the data should be loaded (overwrite everything, keep old data, etc)
        :return a result obj
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

    # def pasteDataFrame(self, anchorCell: CellAddress, dataFrame):
    #     raise NotImplementedError()
    #
    # def pasteDataFrameRs(self, anchorCell: CellAddress, dataFrame) -> Result[None, ErrorReport]:
    #     raise NotImplementedError()

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