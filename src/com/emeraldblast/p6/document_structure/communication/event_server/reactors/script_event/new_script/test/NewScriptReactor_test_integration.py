import unittest

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.script.ScriptContainerErrors import ScriptContainerErrors
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry

from com.emeraldblast.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptRequest import \
    NewScriptRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.script_event.new_script.NewScriptReactor import \
    NewScriptReactor
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.Util import makeGetter
from com.emeraldblast.p6.document_structure.util.for_test.emu.TestEnvImp import TestEnvImp
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class NewScriptReactor_test_integration(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.testEnv = TestEnvImp()
        self.testEnv.startEnv()
        self.wb:Workbook = self.testEnv.app.getWorkbook(0)
        self.app: App = self.testEnv.app
        wbGetter = self.testEnv.app.getBareWorkbookRs
        appGetter = makeGetter(self.testEnv.app)

        self.reactor = NewScriptReactor(wbGetter,appGetter)
    def test_react_add_app_script(self):
        req1 = NewScriptRequest(
            scriptEntry = ScriptEntry(
                key = ScriptEntryKey("s1",None),
                script = "script content 1"
            )
        )

        self.assertFalse(self.app.scriptContainer.contains("s1"))
        res1 = self.reactor.react(req1.toProtoBytes())
        self.assertTrue(self.app.scriptContainer.contains("s1"))
        self.assertFalse(res1.errIndicator.isError)
        self.assertIsNone(res1.errIndicator.errorReport)


        res2 = self.reactor.react(req1.toProtoBytes())
        self.assertTrue(res2.errIndicator.isError)
        self.assertIsNotNone(res2.errIndicator.errorReport)
        self.assertTrue(res2.errIndicator.errorReport.isSameErr(ScriptContainerErrors.ScriptAlreadyExist.header))
        
    def test_react_add_wb_script(self):
        req1 = NewScriptRequest(
            scriptEntry = ScriptEntry(
                key = ScriptEntryKey("s1",self.wb.workbookKey),
                script = "script content 1"
            )
        )

        self.assertFalse(self.wb.scriptContainer.contains("s1"))
        res1 = self.reactor.react(req1.toProtoBytes())
        self.assertTrue(self.wb.scriptContainer.contains("s1"))
        self.assertFalse(res1.errIndicator.isError)
        self.assertIsNone(res1.errIndicator.errorReport)


        res2 = self.reactor.react(req1.toProtoBytes())
        self.assertTrue(res2.errIndicator.isError)
        self.assertIsNotNone(res2.errIndicator.errorReport)
        self.assertTrue(res2.errIndicator.errorReport.isSameErr(ScriptContainerErrors.ScriptAlreadyExist.header))






if __name__ == '__main__':
    unittest.main()
