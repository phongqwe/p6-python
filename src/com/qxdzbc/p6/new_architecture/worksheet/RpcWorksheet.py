from typing import Optional, Union, Tuple

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.BaseWorksheet import BaseWorksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.common.RpcUtils import RpcUtils
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.cell.RpcCell import RpcCell
from com.qxdzbc.p6.new_architecture.rpc.data_structure.BoolMsg import \
    BoolMsg
from com.qxdzbc.p6.new_architecture.rpc.data_structure.Cell2Pr import Cell2Pr
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range import RangeId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.range.RpcRange import RpcRange
from com.qxdzbc.p6.new_architecture.worksheet.msg.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.new_architecture.worksheet.msg.CheckContainAddressRequest import CheckContainAddressRequest
from com.qxdzbc.p6.new_architecture.worksheet.msg.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.new_architecture.worksheet.msg.GetUsedRangeResponse import GetUsedRangeResponse
from com.qxdzbc.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto
from com.qxdzbc.p6.proto.rpc.workbook.service.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.worksheet.service.WorksheetService_pb2_grpc import WorksheetServiceStub


class RpcWorksheet(BaseWorksheet):

    def __init__(
            self,
            name: str,
            wbKey: WorkbookKey,
            stubProvider: RpcStubProvider, ):
        self._name = name
        self._wbk = wbKey
        self._stubProvider = stubProvider

    @property
    def wbKey(self) -> WorkbookKey:
        return self._wbk

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        a = CellAddresses.parse(address)
        return RpcCell(a,self._wbk,self._name,self._stubProvider)

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        a = RangeAddresses.parse(rangeAddress)
        return RpcRange(a,self._wbk,self._name)

    def addCell(self, cell: Cell):
        def f():
            cellValue = cell.cellValue
            fm = None
            if cell.formula:
                fm = cell.formula
            cpr = Cell2Pr(
                id = CellId(cell.address,self._wbk,self._name),
                value =cellValue,
                formula = fm
            )
            self._wssv.addCell(request=cpr.toProtoObj())
        return self._onWsSvOk(f)

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        def f():
            cellId = CellId(address,self._wbk,self._name)
            oProto = self._wssv.deleteCell(request=cellId.toProtoObj())
            o = SingleSignalResponse.fromProto(oProto)
            return o.toRs()
        return self._onWbsvOkRs(f)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        raise NotImplementedError()

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        def f():
            rangeId = RangeId(rangeAddress,self._wbk,self._name)
            oProto = self._wssv.deleteRange(request=rangeId.toProtoObj())
            o = SingleSignalResponse.fromProto(oProto)
            return o.toRs()
        return self._onWbsvOkRs(f)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.containsAddress(address)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.containsAddress(CellAddresses.fromColRow(col,row))

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        def f():
            cellId = CellId(address,self._wbk,self._name)
            oProto = self._wssv.getCell(request=cellId.toProtoObj())
            o = SingleSignalResponse.fromProto(oProto)
            if o.isOk():
                return RpcCell(address,self._wbk,self._name)
            else:
                return None
        return self._onWsSvOk(f)

    def containsAddress(self, address: CellAddress) -> bool:
        def f():
            req = CheckContainAddressRequest(
                wsId = self._id,
                cellAddress = address
            )
            oProto = self._wssv.containAddress(request=req.toProtoObj())
            o = BoolMsg.fromProto(oProto)
            return o.v
        return self._onWsSvOk(f)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.containsAddress(CellAddresses.fromColRow(col, row))

    @property
    def _id(self) -> WorksheetId:
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

    def _onWsSvOk(self, f):
        return RpcUtils.onServiceOk(self._wssv, f)

    def _onWbsvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wbsv, f)

    @property
    def size(self) -> int:
        def f() -> int:
            request = self._id
            out = self._wssv.getCellCount(request = request.toProtoObj())
            countResponse = CellCountResponse.fromProto(out)
            return countResponse.count

        return self._onWsSvOk(f)

    @property
    def cells(self) -> list[Cell]:
        def f() -> list[Cell]:
            request = self._id.toProtoObj()
            oProto = self._wssv.getAllCell(request = request)
            o = GetAllCellResponse.fromProto(oProto)
            rt = []
            for c in o.cellAddressList:
                rt.append(RpcCell(c, self._wbk, self._name,self._stubProvider))
            return rt

        return self._onWsSvOk(f)

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.usedRangeAddress

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        def f() -> RangeAddress:
            request = self._id
            outProto = self._wssv.getUsedRangeAddress(request = request.toProtoObj())
            out = GetUsedRangeResponse.fromProto(outProto)
            r = out.rangeAddress
            return r
        return self._onWsSvOk(f)

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
        def f() -> Result[None, ErrorReport]:
            req = RenameWorksheetRequest(
                wbKey = self._wbk,
                oldName = self._name,
                newName = newName
            )
            outProto: SingleSignalResponseProto = self._wbsv.renameWorksheet(request = req.toProtoObj())
            out = SingleSignalResponse.fromProto(outProto)
            return out.toRs()

        return self._onWbsvOkRs(f)

    def pasteRs(self, cell: CellAddress) -> Result[None, ErrorReport]:
        def f() -> Result[None, ErrorReport]:
            request = CellId(cell,self._wbk,self._name)
            oProto = self._wssv.paste(request = request)
            o = SingleSignalResponse.fromProto(oProto)
            return o.toRs()
        return self._onWsSvOk(f)

    def pasteDataFrameRs(self, anchorCell: CellAddress, dataFrame) -> Result[None, ErrorReport]:
        """todo make a request to update a range"""
        pass

