import unittest


from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.proto.AppProtos_pb2 import LoadWorkbookResponseProto


class LoadWorkbookResponse_test(unittest.TestCase):
    def test_toProto_1(self):
        wbk = WorkbookKeys.fromNameAndPath("wb")
        o = LoadWorkbookResponse(
            wbKey = wbk
        )
        p = o.toProtoObj()
        expect = LoadWorkbookResponseProto(
            wbKey = wbk.toProtoObj()
        )
        self.assertEqual(expect,p)

    def test_toProto_2(self):
        er = ErrorReport(
            header=ErrorHeader("123","Abc")
        )
        o = LoadWorkbookResponse(
            errorReport = er
        )
        p = o.toProtoObj()
        expect = LoadWorkbookResponseProto(
            errorReport = er.toProtoObj()
        )
        self.assertEqual(expect,p)




if __name__ == '__main__':
    unittest.main()
