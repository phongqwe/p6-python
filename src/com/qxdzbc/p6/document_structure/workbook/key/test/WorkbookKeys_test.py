import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class WorkbookKeys_test(unittest.TestCase):
    def test_fromProto(self):
        key1 = WorkbookKeys.fromNameAndPath("name","/path/1/2")
        proto = key1.toProtoObj()
        key2 = WorkbookKeys.fromProto(proto)
        self.assertEqual(key1,key2)


if __name__ == '__main__':
    unittest.main()
