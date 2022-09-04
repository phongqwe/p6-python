import unittest
from pathlib import Path

from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.workbook.Workbooks import Workbooks
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookProto, WorksheetProto, CellProto, CellValueProto


class Workbooks_test(unittest.TestCase):
    def test_FromProto(self):
        wbKey = WorkbookKeys.fromNameAndPath("Book1",None)
        path = Path("pathx")
        ws1 = WorksheetProto(
            name = "Sheet1",
            cell = [
                CellProto(
                    address = CellAddresses.fromLabel("C23").toProtoObj(),
                    value = CellValueProto(str="123qwe"),
                    formula = "formula z",
                ),
                CellProto(
                    address = CellAddresses.fromLabel("N5").toProtoObj(),
                    value = CellValueProto(num=555),
                )
            ]
        )
        proto = WorkbookProto(
            workbookKey = wbKey.toProtoObj(),
            worksheet = [
                ws1
            ],
            scripts = [
                SimpleScriptEntry("s1", "c1").toProtoObj(),
                SimpleScriptEntry("s2", "c2").toProtoObj(),
            ]
        )
        wb = Workbooks.fromProto(proto,path)
        self.assertEqual(WorkbookKeys.fromNameAndPath(wbKey.fileName,path),wb.workbookKey)
        self.assertEqual(1, len(wb.worksheets))

        ws = wb.getWorksheet(0)
        ws.cell("B2").formula="""=SCRIPT(1+2+3)"""
        self.assertEqual(6, ws.cell("B2").value)

        for scriptProto in proto.scripts:
            name = scriptProto.name
            script = scriptProto.script
            self.assertEqual(script,wb.getScript(name))





if __name__ == '__main__':
    unittest.main()
