import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookRequest import \
    SaveWorkbookRequest
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        wbk = WorkbookKeys.fromNameAndPath("a",None)
        proto = SaveWorkbookRequestProto(
            workbookKey = wbk.toProtoObj(),
            path = "qwe"
        )

        o = SaveWorkbookRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(wbk,o.workbookKey)
        self.assertEqual(proto.path, o.path)

if __name__ == '__main__':
    unittest.main()
