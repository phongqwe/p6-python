import unittest


from com.qxdzbc.p6.document_structure.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.CreateNewWorkbookResponse import CreateNewWorkbookResponse


class CreateNewWorkbookResponse_test(unittest.TestCase):

    def test_toProtoObj(self):
        o = CreateNewWorkbookResponse(
            isError = False
        )
        proto = o.toProtoObj()
        self.assertEqual(o.isError, proto.isError)
        self.assertFalse(proto.HasField("errorReport"))
        self.assertFalse(proto.HasField("workbook"))
        self.assertFalse(proto.HasField("windowId"))

    def test_toProtoObj_errorCase(self):
        er = AppErrors.WorkbookNotExist.report("qbc")
        o = CreateNewWorkbookResponse(
            isError = False,
            errorReport = er
        )
        proto = o.toProtoObj()
        self.assertEqual(o.isError, proto.isError)
        self.assertEqual(o.errorReport.toProtoObj(),proto.errorReport)

    # def test_toProtoObj_stdCase(self):
    #     wb = WorkbookImp("abc")
    #     o = CreateNewWorkbookResponse(
    #         isError = False,
    #         workbook = wb
    #     )
    #     proto = o.toProtoObj()
    #     self.assertEqual(wb.toProtoObj(), proto.workbook)

    def test_toProtoObj_validWindowId(self):
        o = CreateNewWorkbookResponse(
            isError = False,
            windowId = "abc"
        )
        proto = o.toProtoObj()
        self.assertEqual(o.windowId, proto.windowId)

        o2 = CreateNewWorkbookResponse(
            isError = False,
            windowId = None
        )
        proto2 = o2.toProtoObj()
        self.assertFalse(proto2.HasField("windowId"))


if __name__ == '__main__':
    unittest.main()
