import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.file.saver.EventP6FileSaver import EventP6FileSaver
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class EventP6FileSaver_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_triggerEvent_stdCase(self):
        cb = MagicMock()
        mockSaver = MagicMock()
        mockSaver.saveRs = MagicMock(return_value = Ok(None))
        saver = EventP6FileSaver(
            saver = mockSaver,
            onSave = cb
        )
        wb = WorkbookImp("Book1", path = Path("folder/file.txt"))
        newPath = Path("folder/file2222.txt")
        saver.saveRs(wb, newPath)
        mockSaver.saveRs.assert_called_once_with(wb, newPath)

        eventData = EventData(
            event = P6Events.Workbook.SaveWorkbook.event,
            data = SaveWorkbookResponse(
                path = str(newPath.absolute()),
                isError = False,
                errorReport = None,
                workbookKey = wb.workbookKey
            )
        )

        cb.assert_called_once_with(eventData)

    def test_triggerEvent_errCase(self):
        cb = MagicMock()
        mockSaver = MagicMock()
        errReport = ErrorReport(
            header = ErrorHeader("123","abc"),
            data = "data data"
        )
        mockSaver.saveRs = MagicMock(return_value = Err(errReport))
        saver = EventP6FileSaver(
            saver = mockSaver,
            onSave = cb
        )
        wb = WorkbookImp("Book1", path = Path("folder/file.txt"))
        newPath = Path("folder/file2222.txt")
        saver.saveRs(wb, newPath)
        mockSaver.saveRs.assert_called_once_with(wb, newPath)

        eventData = EventData(
            event = P6Events.Workbook.SaveWorkbook.event,
            data = SaveWorkbookResponse(
                path = str(newPath.absolute()),
                isError = True,
                errorReport = errReport,
                workbookKey = wb.workbookKey
            )
        )

        cb.assert_called_once_with(eventData)



if __name__ == '__main__':
    unittest.main()
