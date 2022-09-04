import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.file.loader.P6ProtoFileLoader import P6ProtoFileLoader
from com.qxdzbc.p6.document_structure.file.saver.P6ProtoFileSaver import P6ProtoFileSaver
from com.qxdzbc.p6.document_structure.workbook.Workbooks import Workbooks
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookProto, CellProto, WorksheetProto, CellValueProto


class P6ProtoFileSaver_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.filePath = Path("abc.txt")
        self.saver = P6ProtoFileSaver()

    def test_save(self):
        wbKey = WorkbookKeys.fromNameAndPath("Book1", None)
        ws1 = WorksheetProto(
            name = "Sheet1",
            cell = [
                CellProto(
                    address = CellAddresses.fromLabel("@C23").toProtoObj(),
                    value = CellValueProto(str="123qwe"),
                    formula = "formula z",
                ),
                CellProto(
                    address = CellAddresses.fromLabel("@N5").toProtoObj(),
                    value = CellValueProto(num=555),
                )
            ]
        )
        wbProto = WorkbookProto(
            workbookKey = wbKey.toProtoObj(),
            worksheet = [
                ws1
            ],
            scripts = [
                SimpleScriptEntry("s1","c1").toProtoObj(),
                SimpleScriptEntry("s2","c2").toProtoObj(),
            ]
        )

        workbook = Workbooks.fromProto(wbProto)
        if self.filePath.exists():
            os.remove(self.filePath)

        self.assertFalse(self.filePath.exists())
        saveRs = self.saver.saveRs(workbook, self.filePath)
        self.assertTrue(saveRs.isOk())
        self.assertTrue(self.filePath.exists())

        loader = P6ProtoFileLoader()
        loadRs = loader.loadRs(self.filePath)
        self.assertTrue(loadRs.isOk())
        loadedWb = loadRs.value
        self.assertEqual(self.filePath.name,loadedWb.name)
        self.assertEqual(loadedWb.path,self.filePath)
        self.assertEqual(1, loadedWb.sheetCount)
        ws = loadedWb.getWorksheet(0)
        self.assertEqual("Sheet1",ws.name)
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@C23")))
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@N5")))
        self.assertEqual(2,ws.size)

        ws.cell("@A1").value = 123
        self.assertEqual(123,ws.cell("@A1").value)

        ws.cell("@B33").formula="""=SCRIPT(1+2+3)"""
        self.assertEqual(6, ws.cell("@B33").value)

        self.assertEqual(workbook.allScripts,loadedWb.allScripts)

    def test_saveRs_invalidPath(self):
        rs = self.saver.saveRs(MagicMock(),None)
        self.assertTrue(rs.isErr())

    # def test_z(self):
    #     loader = P6ProtoFileLoader()
    #     lrs = loader.loadRs("/home/abc/Documents/gits/project2/p6/b1.txt")
    #     loadedWb = lrs.value
    #     self.assertTrue(len(loadedWb.allScripts)!=0)
if __name__ == '__main__':
    unittest.main()
