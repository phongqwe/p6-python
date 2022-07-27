import unittest

from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.SetActiveWorksheetRequest import \
    SetActiveWorksheetRequest


class SetActiveWorksheetRequest_test(unittest.TestCase):
    def test_toProto_fromProto(self):
        o = SetActiveWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("qwe"),
            wsName = "Sheet1")

        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.wsName,p.wsName)
        self.assertFalse(p.HasField("index"))

        o2 = SetActiveWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("qwe22"),
            index=123
        )
        p2 = o2.toProtoObj()
        self.assertEqual(o2.wbKey.toProtoObj(), p2.wbKey)
        self.assertEqual(o2.index, p2.index)
        self.assertFalse(p2.HasField("wsName"))

        o22 = SetActiveWorksheetRequest.fromProto(p2)
        self.assertEqual(o22,o2)


if __name__ == '__main__':
    unittest.main()
