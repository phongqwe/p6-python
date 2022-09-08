from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider

from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto


class Worksheets:
    @staticmethod
    def fromProto(wsProto:WorksheetProto,stubProvider:RpcStubProvider):
        ws = RpcWorksheet(name = wsProto.name,wbKey = WorkbookKeys.fromProto(wsProto.wbKey),stubProvider = stubProvider)
        return ws