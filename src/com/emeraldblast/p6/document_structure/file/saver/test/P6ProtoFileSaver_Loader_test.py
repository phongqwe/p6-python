import os
import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.file.loader.P6ProtoFileLoader import P6ProtoFileLoader
from com.emeraldblast.p6.document_structure.file.saver.P6ProtoFileSaver import P6ProtoFileSaver
from com.emeraldblast.p6.document_structure.workbook.Workbooks import Workbooks
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.DocProtos_pb2 import WorkbookProto, CellProto, WorksheetProto

from com.emeraldblast.p6.document_structure.file.saver.P6FileSaverStd import P6FileSaverStd
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.WorkbookJson import WorkbookJson



class P6ProtoFileSaver_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.filePath = Path("abc.txt")

    def test_save(self):
        wbKey = WorkbookKeys.fromNameAndPath("Book1", None)
        ws1 = WorksheetProto(
            name = "Sheet1",
            cell = [
                CellProto(
                    address = CellAddresses.fromLabel("@C23").toProtoObj(),
                    value = "123qwe",
                    formula = "formula z",
                    script = "script x"
                ),
                CellProto(
                    address = CellAddresses.fromLabel("@N5").toProtoObj(),
                    value = "555",
                )
            ]
        )
        wbProto = WorkbookProto(
            workbookKey = wbKey.toProtoObj(),
            worksheet = [
                ws1
            ]
        )

        workbook = Workbooks.fromProto(wbProto)
        saver = P6ProtoFileSaver()
        if self.filePath.exists():
            os.remove(self.filePath)

        self.assertFalse(self.filePath.exists())
        saveRs = saver.saveRs(workbook, self.filePath)
        self.assertTrue(saveRs.isOk())
        self.assertTrue(self.filePath.exists())

        loader = P6ProtoFileLoader()
        loadRs = loader.loadRs(self.filePath)
        self.assertTrue(loadRs.isOk())
        loadedWb = loadRs.value
        self.assertEqual(loadedWb.name, workbook.name)
        self.assertEqual(loadedWb.path,self.filePath)
        self.assertEqual(1, loadedWb.worksheetCount)
        ws = loadedWb.getWorksheet(0)
        self.assertEqual("Sheet1",ws.name)
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@C23")))
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@N5")))
        self.assertEqual(2,ws.size)

        ws.cell("@A1").value = 123
        self.assertEqual(123,ws.cell("@A1").value)

        ws.cell("@B33").formula="""=SCRIPT(1+2+3)"""
        self.assertEqual(6, ws.cell("@B33").value)

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.filePath)


if __name__ == '__main__':
    unittest.main()
