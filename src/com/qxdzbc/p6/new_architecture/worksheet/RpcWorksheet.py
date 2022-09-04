from typing import Optional

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.document_structure.copy_paste.paster.Paster import Paster
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.BaseWorksheet import BaseWorksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.common.RpcUtils import RpcUtils
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.CellCountResponse import CellCountResponse
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
    def _id(self)->WorksheetId:
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
        return RpcUtils.onServiceOk(self._wssv,f)

    def _onWbsvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wbsv,f)

    @property
    def size(self) -> int:
        def f()->int:
            request = self._id
            out = self._wssv.getCellCount(request = request.toProtoObj())
            countResponse = CellCountResponse.fromProto(out)
            return countResponse.count
        return self._onWsSvOk(f)

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        def f()->RangeAddress:
            request = self._id
            out = self._wssv.getUsedRangeAddress(request = request.toProtoObj())
            r = RangeAddresses.fromProto(out)
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

    def pasteDataFrameRs(self, anchorCell: CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        pass

    def pasteProtoRs(self, cell: CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        pass

    def pasteRs(self, cell: CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        pass

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
