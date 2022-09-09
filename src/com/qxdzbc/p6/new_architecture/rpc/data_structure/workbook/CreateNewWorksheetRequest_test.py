import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest


class CreateNewWorksheetRequest_test(unittest.TestCase):
    def test_toProto(self):
        o=CreateNewWorksheetRequest(
            workbookKey = WorkbookKeys.fromNameAndPath("q"),
            newWorksheetName = "qwe"
        )
        p = o.toProtoObj()
        self.assertEqual(o.workbookKey.toProtoObj(),p.workbookKey)
        self.assertEqual(o.newWorksheetName,p.newWorksheetName)

        o = CreateNewWorksheetRequest(
            workbookKey = WorkbookKeys.fromNameAndPath("q"),
        )
        p = o.toProtoObj()
        self.assertFalse(p.HasField("newWorksheetName"))



if __name__ == '__main__':
    unittest.main()
