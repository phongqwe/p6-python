import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse
from com.emeraldblast.p6.document_structure.file.loader.EventP6FileLoader import EventP6FileLoader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class EventP6FileLoader_test(unittest.TestCase):

    def test_triggerEvent_stdCase(self):
        cb = MagicMock()
        mockLoader = MagicMock()
        wb = WorkbookImp("file.txt", path = Path("folder/file.txt"))
        mockLoader.loadRs = MagicMock(return_value = Ok(wb))
        loader = EventP6FileLoader(
            loader = mockLoader,
            onLoad = cb
        )

        newPath = Path("folder/file.txt")
        loader.loadRs(newPath)
        mockLoader.loadRs.assert_called_once_with(newPath)

        eventData = LoadWorkbookResponse(
            isError = False,
            errorReport = None,
            windowId = None,
            workbook = wb
        ).toEventData()

        cb.assert_called_once_with(eventData)

    def test_triggerEvent_errCase(self):
        cb = MagicMock()
        mockLoader = MagicMock()
        errReport = ErrorReport(
            header = ErrorHeader("123", "abc"),
            data = "data data"
        )
        mockLoader.loadRs = MagicMock(return_value = Err(errReport))
        loader = EventP6FileLoader(
            loader = mockLoader,
            onLoad = cb
        )
        wb = WorkbookImp("Book1", path = Path("folder/file.txt"))
        newPath = Path("folder/file.txt")
        loader.loadRs(newPath)
        mockLoader.loadRs.assert_called_once_with(newPath)

        eventData = LoadWorkbookResponse(
            isError = True,
            errorReport = errReport,
            workbook = None,
            windowId = None,
        ).toEventData()

        cb.assert_called_once_with(eventData)


if __name__ == '__main__':
    unittest.main()
