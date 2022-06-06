import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.workbook.Workbooks import Workbooks
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.DocProtos_pb2 import WorkbookProto, WorksheetProto, CellProto


class Workbooks_test(unittest.TestCase):
    def test_FromProto(self):
        wbKey = WorkbookKeys.fromNameAndPath("Book1",None)
        path = Path("pathx")
        ws1 = WorksheetProto(
            name = "Sheet1",
            cell = [
                CellProto(
                    address = CellAddresses.fromLabel("@C23").toProtoObj(),
                    value = "123qwe",
                    formula = "formula z",
                ),
                CellProto(
                    address = CellAddresses.fromLabel("@N5").toProtoObj(),
                    value = "555",
                )
            ]
        )
        proto = WorkbookProto(
            workbookKey = wbKey.toProtoObj(),
            worksheet = [
                ws1
            ]
        )
        wb = Workbooks.fromProto(proto,path)
        self.assertEqual(WorkbookKeys.fromNameAndPath(wbKey.fileName,path),wb.workbookKey)
        self.assertEqual(1, len(wb.worksheets))
        ws = wb.getWorksheet(0)
        ws.cell("@B2").formula="""=SCRIPT(1+2+3)"""
        self.assertEqual(6, ws.cell("@B2").value)




if __name__ == '__main__':
    unittest.main()
