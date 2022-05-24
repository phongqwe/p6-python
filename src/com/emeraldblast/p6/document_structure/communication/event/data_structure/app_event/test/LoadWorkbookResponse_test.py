import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import LoadWorkbookResponseProto


class LoadWorkbookResponse_test(unittest.TestCase):
    def test_toProto_1(self):
        wb = WorkbookImp("abc")
        o = LoadWorkbookResponse(
            isError = False,
            workbook = wb
        )
        p = o.toProtoObj()
        expect = LoadWorkbookResponseProto(
            isError = o.isError,
            workbook = wb.toProtoObj()
        )
        self.assertEqual(expect,p)

    def test_toProto_2(self):
        er = ErrorReport(
            header=ErrorHeader("123","Abc")
        )
        o = LoadWorkbookResponse(
            isError = True,
            errorReport = er
        )
        p = o.toProtoObj()
        expect = LoadWorkbookResponseProto(
            isError = o.isError,
            errorReport = er.toProtoObj()
        )
        self.assertEqual(expect,p)




if __name__ == '__main__':
    unittest.main()
