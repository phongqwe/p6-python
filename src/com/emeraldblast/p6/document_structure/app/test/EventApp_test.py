import unittest
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


if __name__ == '__main__':
    unittest.main()
