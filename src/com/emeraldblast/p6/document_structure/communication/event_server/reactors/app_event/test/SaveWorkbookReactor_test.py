import os
import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookRequest import \
    SaveWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook_event.SaveWorkbookReactor import \
    SaveWorkbookReactor
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleApp
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        app = sampleApp()
        def appGetter() -> App:
            return app
        self.app = app

        self.ag = appGetter
        self.filePath = Path("file.txt")
        self.wb = WorkbookImp("file.txt", self.filePath)
        self.ag().wbContainer.addWorkbook(self.wb)



    def tearDown(self) -> None:
        super().tearDown()
        if self.filePath.exists():
            os.remove(self.filePath)

    def test_react_ok(self):
        reactor = SaveWorkbookReactor(appGetter = self.ag)
        oldWbKey = self.wb.workbookKey
        request = SaveWorkbookRequestProto(
            workbookKey = self.wb.workbookKey.toProtoObj(),
            path = str(self.wb.path.absolute())
        )
        self.assertFalse(self.filePath.exists())
        rt = reactor.react(request.SerializeToString())
        self.assertFalse(rt.isError)
        self.assertTrue(self.filePath.exists())
        self.assertEqual(rt.workbookKey, oldWbKey)

    def test_react_differentPath(self):
        reactor = SaveWorkbookReactor(appGetter = self.ag)
        oldWbKey = self.wb.workbookKey
        dp = Path("f2.txt")
        request = SaveWorkbookRequestProto(
            workbookKey = self.wb.workbookKey.toProtoObj(),
            path = str(dp.absolute())
        )
        rt = reactor.react(request.SerializeToString())
        self.assertFalse(rt.isError)
        self.assertEqual(rt.workbookKey, oldWbKey)

        nkey=WorkbookKeys.fromNameAndPath(str(dp.name),dp)
        print(self.app.getWorkbook(nkey).workbookKey)
        if dp.exists():
            os.remove(dp)




if __name__ == '__main__':
    unittest.main()
