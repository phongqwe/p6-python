from typing import Optional, Union, Tuple

import numpy
import pandas

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.BaseWorksheet import BaseWorksheet
from com.qxdzbc.p6.worksheet.IndWorksheet import IndWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.WorksheetProtoMapping import WorksheetProtoMapping
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.cell.RpcCell import RpcCell
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import \
    BoolMsg
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.LoadDataRequest import LoadDataRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.rpc.data_structure.range.RangeId import RangeId
from com.qxdzbc.p6.rpc.data_structure.workbook.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.range.RpcRange import RpcRange
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.CheckContainAddressRequest import CheckContainAddressRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetUsedRangeResponse import GetUsedRangeResponse
from com.qxdzbc.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto, IndCellProto
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class InternalRpcWorksheet(BaseWorksheet):

    def __init__(
            self,
            name: str,
            wbKey: WorkbookKey,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):
        self._name = name
        self._wbk = wbKey
        self._stubProvider = stubProvider

    def _makeLoadDataRequestRs(self, cells: list[IndCell], anchorCell: CellAddress, loadType: LoadType) -> \
            Result['Worksheet', ErrorReport]:
        request = LoadDataRequest(
            loadType = loadType,
            ws = IndWorksheet(
                id = WorksheetId(
                    wsName = self.name,
                    wbKey = self.wbKey,
                ),
                cells = cells
            ),
            anchorCell = anchorCell
        )
        oProto = self._wssv.loadData(request = request.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        if o.isOk():
            return Ok(self)
        else:
            return Err(o.errorReport)

    def load2DArrayRs(self, dataAray, anchorCell: CellAddress = CellAddresses.A1,
                      loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> \
            Result['Worksheet', ErrorReport]:
        is2D = len(numpy.shape(dataAray)) == 2
        anchorRow = anchorCell.rowIndex
        anchorCol = anchorCell.colIndex
        cpmList = []
        if is2D:
            # x: construct cpmList, each sub array is treated as a row
            for (r, arrayRow) in enumerate(dataAray):
                for (c, item) in enumerate(arrayRow):
                    targetCellAddress: CellAddress = CellAddresses.fromColRow(anchorCol + c, anchorRow + r)
                    cpmList.append(IndCell(
                        address = targetCellAddress,
                        value = CellValue.fromAny(item)
                    ))
            return self._makeLoadDataRequestRs(cpmList, anchorCell, loadType)
        else:
            return Err(CommonErrors.WrongTypeReport.report("data obj is not 2D"))

    def loadDataFrameRs(
            self, dataFrame,
            anchorCell: CellAddress = CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader: bool = True,
    ) -> Result['Worksheet', ErrorReport]:
        # x: a dataframe is always 2d so, no need to check its dimension
        df = dataFrame
        isPandasDataFrame = isinstance(df, pandas.core.frame.DataFrame)
        anchorCol = anchorCell.colIndex
        anchorRow = anchorCell.rowIndex
        if isPandasDataFrame:
            cpmList = []
            headerCpmList = []
            rowOffset = 0
            if keepHeader:
                rowOffset = 1
                # x: construct header cells
                for (i, header) in enumerate(list(df.columns)):
                    cpm = IndCell(
                        address = CellAddresses.fromColRow(
                            anchorCol + i,
                            anchorRow
                        ),
                        value = CellValue.fromStr(str(header))
                    )
                    headerCpmList.append(cpm)

            # x: construct cpmList
            for colIndex in df:
                col = df[colIndex]
                for (rowIndex, item) in enumerate(col):
                    cpm = IndCell(
                        address = CellAddresses.fromColRow(
                            anchorCol + colIndex,
                            anchorRow + rowIndex + rowOffset),
                        value = CellValue.fromAny(item)
                    )
                    cpmList.append(cpm)
            return self._makeLoadDataRequestRs(headerCpmList + cpmList, anchorCell, loadType)
        else:
            return Err(CommonErrors.WrongTypeReport.report("dataFrame obj is not a pandas DataFrame"))

    def toProtoObj(self) -> WorksheetProto:
        return WorksheetProto(
            name = self._name,
            wbKey = self._wbk.toProtoObj(),
        )

    @property
    def wbKey(self) -> WorkbookKey:
        return self._wbk

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        a = CellAddresses.parse(address)
        return RpcCell(a, self._wbk, self._name, self._stubProvider)

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        a = RangeAddresses.parse(rangeAddress)
        return RpcRange(a, self._wbk, self._name)

    def addCellRs(self, cell: Cell) -> Result[None, ErrorReport]:
        newCellId = CellId(cell.address, self.wbKey, self.name)
        cellProto = cell.toProtoObj()
        cellProto.id.CopyFrom(newCellId.toProtoObj())
        oProto = self._wssv.addCell(request = cellProto)
        o = SingleSignalResponse.fromProto(oProto)
        oRs = o.toRs()
        return oRs

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        cellId = CellId(address, self._wbk, self._name)
        oProto = self._wssv.deleteCell(request = cellId.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        return o.toRs()

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        raise NotImplementedError()

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        rangeId = RangeId(rangeAddress, self._wbk, self._name)
        oProto = self._wssv.deleteRange(request = rangeId.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        return o.toRs()

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.containsAddress(address)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.containsAddress(CellAddresses.fromColRow(col, row))

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        cellId = CellId(address, self._wbk, self._name)
        oProto = self._wssv.getCell(request = cellId.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        if o.isOk():
            return RpcCell(address, self._wbk, self._name)
        else:
            return None

    def containsAddress(self, address: CellAddress) -> bool:
        req = CheckContainAddressRequest(
            wsId = self.id,
            cellAddress = address
        )
        oProto = self._wssv.containAddress(request = req.toProtoObj())
        o = BoolMsg.fromProto(oProto)
        return o.v

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.containsAddress(CellAddresses.fromColRow(col, row))

    @property
    def id(self) -> WorksheetId:
        return WorksheetId(
            wbKey = self._wbk,
            wsName = self._name,
        )

    @property
    def _wbsv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    @property
    def _wssv(self) -> Optional[WorksheetServiceStub]:
        return self._stubProvider.wsService

    @property
    def size(self) -> int:
        request = self.id
        out = self._wssv.getCellCount(request = request.toProtoObj())
        countResponse = CellCountResponse.fromProto(out)
        return countResponse.count

    @property
    def cells(self) -> list[Cell]:
        request = self.id.toProtoObj()
        oProto = self._wssv.getAllCell(request = request)
        o = GetAllCellResponse.fromProto(oProto)
        rt = []
        for c in o.cellAddressList:
            rt.append(RpcCell(c, self._wbk, self._name, self._stubProvider))
        return rt

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.usedRangeAddress

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        request = self.id
        outProto = self._wssv.getUsedRangeAddress(request = request.toProtoObj())
        out = GetUsedRangeResponse.fromProto(outProto)
        r = out.rangeAddress
        return r

    @property
    def maxUsedCol(self) -> int | None:
        usedRange = self.usedRangeAddress
        return usedRange.lastColIndex

    @property
    def minUsedCol(self) -> int | None:
        usedRange = self.usedRangeAddress
        return usedRange.firstColIndex

    @property
    def maxUsedRow(self) -> int | None:
        usedRange = self.usedRangeAddress
        return usedRange.lastRowIndex

    @property
    def minUsedRow(self) -> int | None:
        usedRange = self.usedRangeAddress
        return usedRange.firstRowIndex

    @property
    def name(self) -> str:
        return self._name

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        req = RenameWorksheetRequest(
            wbKey = self._wbk,
            oldName = self._name,
            newName = newName
        )
        outProto: SingleSignalResponseProto = self._wbsv.renameWorksheet(request = req.toProtoObj())
        out = SingleSignalResponse.fromProto(outProto)
        return out.toRs()

    def pasteRs(self, cell: CellAddress) -> Result[None, ErrorReport]:
        request = CellId(cell, self._wbk, self._name)
        oProto = self._wssv.paste(request = request)
        o = SingleSignalResponse.fromProto(oProto)
        return o.toRs()
