import unittest

from bicp_document_structure.app.GlobalScope import setIPythonGlobals
from bicp_document_structure.app.UserFunctions import *
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData


class UserFunctions_test(unittest.TestCase):
    """
    these tests emulate code execution from the front end
    """

    def setUp(self) -> None:
        super().setUp()
        setIPythonGlobals(globals())
        startApp()
        restartApp()
        getApp().createNewWorkbook("Book1")
        getActiveWorkbook().createNewWorksheet("Sheet1")

    def test_trigger_event_on_cell(self):
        app: App = getApp()
        self.a = 0

        def onCellChange(dt: CellEventData):
            self.a += 1

        app.eventReactorContainer.addReactor(
            P6Events.Cell.Update.event,
            EventReactorFactory.makeCellReactor(onCellChange))
        c1 = cell("@A1")
        c1.value = 123
        self.assertEqual(1, self.a)

    def test_B(self):
        cell("@A1").value = 123.0
        getWorkbook("Book1").reRun()
        str(getWorkbook("Book1").toJson())
        cell("@B1").script = """
        cell("@A1").value
        """.strip()
        getWorkbook("Book1").reRun()
        str(getWorkbook("Book1").toJson())

    def test_codeExecution_directLiteral(self):
        cell("@A1").script = "100"
        self.assertEqual(100, cell("@A1").value)

    def test_codeExecution_functionCall(self):
        cell("@A1").script = "len([1,2,3])"
        self.assertEqual(3, cell("@A1").value)

    def test_gettingWbJsonAfterExecution(self):
        book = getWorkbook("Book1")
        cell("@A1").value = 1
        getWorkbook("Book1").reRun()
        j = getWorkbook("Book1").toJson()
        print(j)

    def test_onGlobalScope(self):
        # startApp()
        activeBook = getActiveWorkbook()
        activeBook.setActiveWorksheet("Sheet1")
        sheet = getActiveSheet()
        cellA1_1 = sheet.cell((1, 1))  # A1
        cellA1_1.script = "x=1;x+10"
        cellA1_1.runScript()
        cellA1_2 = cell("@A1")
        self.assertEqual(11, cellA1_2.value)

        cellA1_1.script = "x=2;x*50"
        self.assertEqual(None, cellA1_1.bareValue())

        cellA2 = cell("@A2")
        cellA2.setScriptAndRun("cell(\"@A1\").value+1")
        self.assertEqual(101, cellA2.value)
        self.assertEqual(100, cellA1_1.value)

        cellA3 = cell("@A3")
        cellA3.script = "cell(\"@A1\").value+ cell(\"@A2\").value"
        self.assertEqual(201, cellA3.value)

        cellA1_1.script = "cell(\"@A1\").value"
        self.assertTrue(isinstance(cellA1_1.value, Exception))
        print(cellA1_2.displayValue)

        cellA4 = cell("@A4")
        cellA4.script = "cell(\"@A1\").value + 3"
        self.assertTrue(isinstance(cellA4.value, Exception))
        print(cellA4.displayValue)

    def test_listWorkSheet(self):
        print(listWorksheet("Book1"))
        print(listWorksheet())
        print(listWorkbook())
