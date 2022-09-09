from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import AddWorksheetRequestProto


@dataclass
class AddWorksheetRequest(ToProto[AddWorksheetRequestProto]):
    wbKey: WorkbookKey
    worksheet: Worksheet

    def toProtoObj(self) -> AddWorksheetRequestProto:
        return AddWorksheetRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            worksheet = self.worksheet.toProtoObj()
        )
    
    @staticmethod
    def fromProto(
            proto:AddWorksheetRequestProto,
    ):
        return AddWorksheetRequest(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            worksheet = Worksheets.fromProto(proto.worksheet)
        )
