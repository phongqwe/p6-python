import unittest

from com.qxdzbc.p6.document_structure.communication.event.data_structure.WsWb import WsWb
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class WsWb_test(unittest.TestCase):
    def test_toProto_fromProto(self):
        wswb = WsWb(
            workbookKey = WorkbookKeys.fromNameAndPath(""),
            worksheetName = "S1"
        )
        proto = wswb.toProtoObj()
        self.assertEqual(wswb.workbookKey.toProtoObj(),proto.workbookKey)
        self.assertEqual(wswb.worksheetName,proto.worksheetName)

        wswb2 = WsWb.fromProto(proto)
        self.assertEqual(wswb,wswb2)




if __name__ == '__main__':
    unittest.main()
