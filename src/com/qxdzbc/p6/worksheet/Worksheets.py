from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys

from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto


class Worksheets:
    @staticmethod
    def fromProto(wsProto:WorksheetProto):
        ws = RpcWorksheet(name = wsProto.name,wbKey = WorkbookKeys.fromProto(wsProto.wbKey))
        return ws