from pathlib import Path
from typing import Union

from com.qxdzbc.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry

from com.qxdzbc.p6.document_structure.cell.Cells import Cells
from com.qxdzbc.p6.document_structure.file.P6Files import P6Files
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookProto


class Workbooks:
    @staticmethod
    def fromProto(proto: WorkbookProto, filePath: Path | None = None) -> Workbook:
        wbName = proto.workbookKey.name

        wb = RpcWorkbook(
            name = wbName,
            path = filePath,
        )
        return wb