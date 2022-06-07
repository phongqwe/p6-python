import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.CloseWorkbookReactor import \
    CloseWorkbookReactor
from com.emeraldblast.p6.document_structure.util.Util import makeGetter
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CloseWorkbookRequestProto


class CloseWorkbookReactor_test(unittest.TestCase):
    def test_react(self):
        wbKey = WorkbookKeys.fromNameAndPath("B1")
        app = MagicMock()
        app.rootApp = app
        app.closeWorkbookRs = MagicMock(return_value=Ok(wbKey))
        
        reactor = CloseWorkbookReactor(makeGetter(app))
        req = CloseWorkbookRequestProto(
            workbookKey = wbKey.toProtoObj(),
            windowId = "qwe"
        )
        response = reactor.react(req.SerializeToString())
        self.assertFalse(response.isError)
        self.assertEqual(wbKey,response.workbookKey)
        self.assertIsNone(response.errorReport)

    def test_react_error(self):
        wbKey = WorkbookKeys.fromNameAndPath("B1")
        err =ErrorReport(header=ErrorHeader("123","asd"))
        app = MagicMock()
        app.rootApp = app
        app.closeWorkbookRs = MagicMock(return_value = Err(err))

        reactor = CloseWorkbookReactor(makeGetter(app))
        req = CloseWorkbookRequestProto(
            workbookKey = wbKey.toProtoObj(),
            windowId = "qwe"
        )
        response = reactor.react(req.SerializeToString())
        self.assertTrue(response.isError)
        self.assertEqual(wbKey, response.workbookKey)
        self.assertEqual(err, response.errorReport)

        


if __name__ == '__main__':
    unittest.main()
