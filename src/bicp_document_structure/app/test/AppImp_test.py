import os
import unittest
from pathlib import Path

from bicp_document_structure.app.AppImp import AppImp
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp
from bicp_document_structure.worksheet.Worksheet import Worksheet


class AppImp_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.app = AppImp()
        self.aa = 0

    def test_createNewWorkbook(self):
        app = self.app
        rs0 = app.createNewWorkbookRs()
        self.assertTrue(rs0.isOk())
        self.assertIsNotNone(rs0.value)
        self.assertEqual("Workbook0", rs0.value.name)
        rs1 = app.createNewWorkbookRs()
        self.assertEqual("Workbook1", rs1.value.name)

    def test_hasWorkbook(self):
        app = AppImp()
        self.assertTrue(app.hasNoWorkbook())
        app.createNewWorkbook()
        self.assertFalse(app.hasNoWorkbook())

    def test_activeWorkbook(self):
        app = self.app
        # x: no active workbook
        self.assertIsNone(app.activeWorkbook)

        # x: get default active workbook
        newWbRs = app.createNewWorkbookRs()
        self.assertEqual(newWbRs.value, app.activeWorkbook)

        # x: active workbook when adding new workbook
        newWbRs2 = app.createNewWorkbookRs()
        self.assertEqual(newWbRs.value, app.activeWorkbook)

        # x: switch active workbook
        app.setActiveWorkbook(1)
        self.assertEqual(newWbRs2.value, app.activeWorkbook)

        # x: set invalid active workbook
        setRs = app.setActiveWorkbookRs(100)
        self.assertTrue(setRs.isErr())
        with self.assertRaises(Exception):
            app.setActiveWorkbook(100)

        # x: active workbook after faulty operation
        self.assertEqual(app.getWorkbook(1), app.activeWorkbook)

    def test_saveWorkbookAtPath(self):
        app = self.app
        fileName = "book1.txt"
        path = Path(fileName)
        book1 = app.createNewWorkbookRs("Book1").value
        saveRs = app.saveWorkbookAtPathRs("Book1",fileName)

        self.assertTrue(saveRs.isOk())
        self.assertTrue(path.exists())
        os.remove(path)

        saveRs2=app.saveWorkbookAtPathRs("Book1",Path(fileName))
        self.assertTrue(saveRs2.isOk())
        self.assertTrue(path.exists())
        os.remove(path)

        saveRs3=app.saveWorkbookAtPathRs("Book1xxx",Path(fileName))
        self.assertFalse(saveRs3.isOk())

        with self.assertRaises(Exception):
            app.saveWorkbookAtPath("invalid workbook", Path(fileName))

    def test_saveWorkbook(self):
        app = self.app
        fileName = "book1.txt"
        path = Path(fileName)
        book1 = app.createNewWorkbookRs("Book1").value
        key = WorkbookKeyImp("Book1",path)
        book1.workbookKey = key
        app.refreshContainer()

        app.saveWorkbook(0)
        self.__testFileExistence(path)
        with self.assertRaises(Exception):
            app.saveWorkbook(100)

        app.saveWorkbook("Book1")
        self.__testFileExistence(path)

        app.saveWorkbook(key)
        self.__testFileExistence(path)

    def test_loadWorkbook(self):

        app = self.app
        fileName = "file.txt"

        # x: load a valid file with result function
        loadRs0=app.loadWorkbookRs(fileName)
        self.assertTrue(loadRs0.isOk())
        self.assertIsNotNone(app.getWorkbook(0))

        # x: load an invalid file with result function
        app = AppImp()
        loadRs2 = app.loadWorkbookRs("invalid file")
        self.assertTrue(loadRs2.isErr())
        self.assertIsNone(app.getWorkbook(0))

        # x: load valid file with normal function
        app = AppImp()
        app.loadWorkbook(fileName)
        self.assertIsNotNone(app.getWorkbook(0))

        # x: load invalid file with normal function
        app = AppImp()
        with self.assertRaises(Exception):
            app.loadWorkbook("invalid file")
        self.assertIsNone(app.getWorkbook(0))

    def test_closeWorkbook(self):
        app = self.app
        app.createNewWorkbook("Book1")
        self.assertIsNotNone(app.getWorkbook("Book1"))
        app.closeWorkbook("Book1")
        self.assertIsNone(app.getWorkbook("Book1"))

        app.createNewWorkbook("Book2")
        self.assertIsNotNone(app.getWorkbook("Book2"))
        rs = app.closeWorkbookRs("Book2")
        self.assertTrue(rs.isOk())
        self.assertEqual(WorkbookKeyImp("Book2"),rs.value)

    def test_forceLoad(self):
        app = self.app
        app.createNewWorkbook("workbookName")
        wb = app.getWorkbook("workbookName")
        wb.workbookKey = WorkbookKeyImp("file.txt",Path("file.txt"))
        app.refreshContainer()
        loadRs = app.forceLoadWorkbookRs("file.txt")
        self.assertTrue(loadRs.isOk())
        self.assertNotEqual(wb, app.getWorkbook("workbookName"))

    def test_listBook(self):
        app = self.app
        app.createNewWorkbook("Book1")
        app.createNewWorkbook("Book2")
        print(app.listWorkbook())

    def __testFileExistence(self,path):
        self.assertTrue(path.exists())
        os.remove(path)


    def onCellChange(self,wb:Workbook,ws:Worksheet,cell:Cell,event:P6Event):
        self.aa = 123

    def __onCellChange(self, wb: Workbook, ws: Worksheet, cell: Cell, event: P6Event):
        self.aa = f"{wb.name}, {ws.name}, {cell.address.label}, {event.code}"

    def test_event_listener_on_loaded_wb(self):

        app = AppImp(onCellChange = self.onCellChange)
        fileName = "file.txt"

        # x: load a valid file with result function
        loadRs0=app.loadWorkbookRs(fileName)
        self.assertTrue(loadRs0.isOk())
        self.assertIsNotNone(app.getWorkbook(0))
        wb:Workbook = loadRs0.value
        sheet = wb.getWorksheet(0)
        self.assertEqual(0,self.aa)
        cell = sheet.cell(CellIndex(1,1))
        cell.value="abc"
        self.assertEqual(123, self.aa)






if __name__ == '__main__':
    unittest.main()
