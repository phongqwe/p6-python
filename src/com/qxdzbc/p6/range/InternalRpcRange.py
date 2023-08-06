from typing import Union, Tuple, Optional

import numpy
import pandas

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.RpcCell import RpcCell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import SingleSignalResponse
from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.rpc_data_structure.MultiCellUpdateRequest import MultiCellUpdateRequest


class InternalRpcRange(Range):

    def _makeAssignmentRequestRs(self,updateEntries:list[IndCell])->Result[None, ErrorReport]:
        request = MultiCellUpdateRequest(
            wsId = self.wsId,
            updateEntries = updateEntries
        )
        oProto = self._wssv.updateMultiCellContent(request = request.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        return o.toRs()

    def assign2dArrayRs(self, data2DArray) -> Result[None, ErrorReport]:
        is2D = len(numpy.shape(data2DArray)) == 2
        if is2D:
            colCount = self.lastCol-self.firstCol + 1
            rowCount = self.lastRow - self.firstRow + 1
            anchorCell: CellAddress = self.rangeAddress.topLeft
            actualRowCount = min(rowCount, len(data2DArray))
            updateEntries = []
            # x: prepare update entry list
            # x: each sub array is treated as a row
            for r in range(actualRowCount):
                cellRowIndex = anchorCell.rowIndex + r
                row = data2DArray[r]
                actualColCount = min(colCount, len(row))
                for c in range(actualColCount):
                    cellColIndex = anchorCell.colIndex + c
                    cellUpdateEntry = IndCell(
                        address = CellAddresses.fromColRow(cellColIndex,cellRowIndex),
                        content = CellContent.fromAny(data2DArray[r][c])
                    )
                    updateEntries.append(cellUpdateEntry)

            # x: make request
            return self._makeAssignmentRequestRs(updateEntries)
        else:
            return Err(CommonErrors.WrongTypeError.report("data obj is not 2D"))

    def assignDataFrameRs(self, dataFrame) -> Result[None, ErrorReport]:
        # pass
        df = dataFrame
        isPandasDataFrame = isinstance(df, pandas.core.frame.DataFrame)

        if isPandasDataFrame:
            anchorCell = self.rangeAddress.topLeft
            anchorCol = anchorCell.colIndex
            anchorRow = anchorCell.rowIndex

            colCount = self.lastCol - self.firstCol + 1
            rowCount = self.lastRow - self.firstRow + 1

            dataColCount = len(df.columns)
            dataRowCount = len(df)

            actualRowCount = min(rowCount, dataRowCount)
            actualColCount = min(colCount,dataColCount)
            # iloc (row - col)
            actualDf = df.iloc[0:actualRowCount, 0:actualColCount]
            updateEntries = []

            rowOffset = 0
            # x: construct cpmList
            for (colIndex, colLabel) in enumerate(list(actualDf.columns)):
                col = actualDf[colLabel]
                for (rowIndex, item) in enumerate(col):
                    ue = IndCell(
                        address = CellAddresses.fromColRow(
                            anchorCol + colIndex,
                            anchorRow + rowIndex + rowOffset),
                        content = CellContent.fromAny(item)
                    )
                    updateEntries.append(ue)
            return self._makeAssignmentRequestRs(updateEntries)
        else:
            return Err(CommonErrors.WrongTypeError.report("the input obj is not a pandas DataFrame"))

    def getCellAtAddress(self, address: CellAddress) -> Optional[Cell]:
        if self.containsAddress(address):
            return RpcCell(
                cellAddress = address,
                wbKey = self.wbKey,
                wsName = self.wsName,
                stubProvider = self._sp
            )
        else:
            return None

    @property
    def wsName(self) -> str:
        return self._wsName

    @property
    def wbKey(self) -> WorkbookKey:
        return self._wbk

    @property
    def rangeAddress(self) -> RangeAddress:
        return self._address

    def __init__(
            self, rangeAddress: RangeAddress,
            wbKey: WorkbookKey,
            wsName: str,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()
    ):
        self._address = rangeAddress
        self._wbk = wbKey
        self._wsName = wsName
        self._sp = stubProvider

    @property
    def _wssv(self) -> Optional[WorksheetServiceStub]:
        return self._sp.wsService

    @property
    def rootRange(self) -> 'Range':
        return self

