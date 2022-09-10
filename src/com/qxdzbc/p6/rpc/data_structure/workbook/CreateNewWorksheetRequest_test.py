import unittest

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.workbook.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest


class CreateNewWorksheetRequest_test(unittest.TestCase):
    def test_toProto(self):
        o=CreateNewWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("q"),
            newWorksheetName = "qwe"
        )
        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertEqual(o.newWorksheetName,p.newWorksheetName)

        o = CreateNewWorksheetRequest(
            wbKey = WorkbookKeys.fromNameAndPath("q"),
        )
        p = o.toProtoObj()
        self.assertFalse(p.HasField("newWorksheetName"))



if __name__ == '__main__':
    unittest.main()
