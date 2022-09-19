import unittest

from com.qxdzbc.p6.util.for_test import TestUtils
from com.qxdzbc.p6.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.qxdzbc.p6.app.rpc_data_structure.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse


class WorkbookKeyWithErrorResponse_test(unittest.TestCase):
    def test_something(self):
        o=WorkbookKeyWithErrorResponse(
            wbKey = WorkbookKeyImp("a"),
        )
        p = o.toProtoObj()
        self.assertEqual(o.wbKey.toProtoObj(),p.wbKey)
        self.assertFalse(p.HasField("errorReport"))
        o2 = WorkbookKeyWithErrorResponse.fromProto(p)
        self.assertEqual(o,o2)

        o3 =WorkbookKeyWithErrorResponse(
            errorReport = TestUtils.TestErrorReport
        )

        p3 = o3.toProtoObj()
        self.assertFalse(p3.HasField("wbKey"))
        self.assertEqual(o3.errorReport.toProtoObj(), p3.errorReport)



if __name__ == '__main__':
    unittest.main()
