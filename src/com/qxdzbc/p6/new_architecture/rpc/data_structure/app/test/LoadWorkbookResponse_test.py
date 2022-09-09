import unittest


from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.AppEventProtos_pb2 import LoadWorkbookResponseProto


class LoadWorkbookResponse_test(unittest.TestCase):
    pass
    # def test_toProto_1(self):
    #     wb = RpcWorkbook("abc",None)
    #     o = LoadWorkbookResponse(
    #         isError = False,
    #         windowId = "123",
    #         workbook = wb
    #     )
    #     p = o.toProtoObj()
    #     expect = LoadWorkbookResponseProto(
    #         isError = o.isError,
    #         windowId="123",
    #         workbook = wb.toProtoObj()
    #     )
    #     self.assertEqual(expect,p)
    #
    # def test_toProto_2(self):
    #     er = ErrorReport(
    #         header=ErrorHeader("123","Abc")
    #     )
    #     o = LoadWorkbookResponse(
    #         isError = True,
    #         windowId = "123",
    #         errorReport = er
    #     )
    #     p = o.toProtoObj()
    #     expect = LoadWorkbookResponseProto(
    #         isError = o.isError,
    #         windowId = "123",
    #         errorReport = er.toProtoObj()
    #     )
    #     self.assertEqual(expect,p)




if __name__ == '__main__':
    unittest.main()
