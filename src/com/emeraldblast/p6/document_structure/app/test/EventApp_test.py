import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.app.EventApp import EventApp

from com.emeraldblast.p6.document_structure.app.AppImp import AppImp
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleApp


class EventApp_test(unittest.TestCase):
    def test_emit_event_when_create_new_wb(self):
        app = AppImp()
        onEvent= MagicMock()
        eventApp = EventApp(app,onEvent)

        eventApp.createNewWorkbookRs("Name")
        onEvent.assert_called_once()
        eventData = onEvent.call_args[0][0]
        self.assertEqual(P6Events.App.CreateNewWorkbook.event,eventData.event)

        eventApp.createDefaultNewWorkbookRs()
        self.assertEqual(2,onEvent.call_count)

        eventApp.createDefaultNewWorkbook()
        self.assertEqual(3,onEvent.call_count)

        eventApp.createNewWorkbook()
        self.assertEqual(4, onEvent.call_count)

    def test_emit_event_when_close_wb(self):
        app = sampleApp()
        onEvent = MagicMock()
        eventApp = EventApp(app, onEvent)
        eventApp.closeWorkbookRs(0)
        self.assertEqual(1,onEvent.call_count)
        eventData = onEvent.call_args[0][0]
        self.assertEqual(P6Events.App.CloseWorkbook.event, eventData.event)

        eventApp.closeWorkbook(0)
        self.assertEqual(2, onEvent.call_count)

        # onEvent is not called when fail to close any wb
        eventApp.closeWorkbookRs(1000)
        self.assertEqual(2,onEvent.call_count)

    def test_saveEvent(self):
        """ensure that save notifier is trigger when a workbook is saved"""
        app = sampleApp(
            saver = MagicMock(),
            loader = MagicMock()
        )
        onEvent = MagicMock()
        eventApp = EventApp(app, onEvent)

        # runSave(app,onEvent)
        path = Path("b1")
        app.createNewWorkbook("b1")
        eventApp.saveWorkbookAtPathRs("b1", path)
        self.assertEqual(1, onEvent.call_count)

        eventApp.saveWorkbookAtPath("b1", path)
        self.assertEqual(2, onEvent.call_count)

        eventApp.saveWorkbook("b1")
        self.assertEqual(3, onEvent.call_count)

        eventApp.saveWorkbookRs("b1")
        self.assertEqual(4, onEvent.call_count)

        if path.exists():
            os.remove(path)

    def test_loadEvent(self):
        """ensure that save notifier is trigger when a workbook is saved"""
        app = sampleApp(
            saver = MagicMock(),
            loader = MagicMock()
        )
        onEvent = MagicMock()
        eventApp = EventApp(app, onEvent)

        path = Path("fileProto2.txt")
        eventApp.loadWorkbookRs(path)
        self.assertEqual(1, onEvent.call_count)

        eventApp.loadWorkbook(Path("fileProto3.txt"))
        self.assertEqual(2, onEvent.call_count)


if __name__ == '__main__':
    unittest.main()
