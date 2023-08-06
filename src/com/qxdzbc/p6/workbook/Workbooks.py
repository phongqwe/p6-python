from pathlib import Path

from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookProto


class Workbooks:
    @staticmethod
    def fromProto(proto: WorkbookProto, filePath: Path | None = None) -> Workbook:
        wbName = proto.key.name

        wb = RpcWorkbook.fromNameAndPath(
            name = wbName,
            path = filePath,
        )
        return wb