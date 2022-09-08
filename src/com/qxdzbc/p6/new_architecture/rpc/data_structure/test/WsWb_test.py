import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.WsWb import WsWb


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
