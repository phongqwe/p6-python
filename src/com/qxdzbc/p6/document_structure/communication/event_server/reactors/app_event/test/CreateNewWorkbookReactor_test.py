import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.CreateNewWorkbookReactor import \
    CreateNewWorkbookReactor
from com.qxdzbc.p6.document_structure.util.Util import makeGetter
from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.qxdzbc.p6.proto.AppEventProtos_pb2 import CreateNewWorkbookRequestProto


class CreateNewWorkbookReactor_test(unittest.TestCase):
    def test_react_stdCase(self):
        app = MagicMock()
        app.rootApp = app
        wb=WorkbookImp("b1")
        app.createDefaultNewWorkbookRs = MagicMock(return_value=Ok(wb))
        
        reactor = CreateNewWorkbookReactor(appGetter = makeGetter(app))
        inputProto = CreateNewWorkbookRequestProto(windowId = "windowId")
        o = reactor.react(inputProto.SerializeToString())
        self.assertFalse(o.isError)
        self.assertEqual(wb, o.workbook)
        self.assertIsNone(o.errorReport)
        self.assertEqual(inputProto.windowId, o.windowId)

    def test_react_errorCase(self):
        app = MagicMock()
        app.rootApp = app
        err = ErrorReport(header=ErrorHeader("123","abc"))
        app.createDefaultNewWorkbookRs = MagicMock(return_value = Err(err))
        reactor = CreateNewWorkbookReactor(appGetter = makeGetter(app))
        inputProto = CreateNewWorkbookRequestProto(windowId = "windowId")
        o = reactor.react(inputProto.SerializeToString())
        self.assertTrue(o.isError)
        self.assertIsNone(o.workbook)
        self.assertTrue(o.errorReport.isSameErr(err))
        self.assertEqual(inputProto.windowId, o.windowId)



if __name__ == '__main__':
    unittest.main()
