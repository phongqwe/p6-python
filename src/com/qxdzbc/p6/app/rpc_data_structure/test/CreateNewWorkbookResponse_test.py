import unittest


from com.qxdzbc.p6.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookResponse import CreateNewWorkbookResponse


class CreateNewWorkbookResponse_test(unittest.TestCase):

    def test_toProtoObj(self):
        o = CreateNewWorkbookResponse(
        )
        proto = o.toProtoObj()
        self.assertFalse(proto.HasField("errorReport"))
        self.assertFalse(proto.HasField("wbKey"))
        self.assertFalse(proto.HasField("windowId"))

    def test_toProtoObj_errorCase(self):
        er = AppErrors.WorkbookNotExist.report("qbc")
        o = CreateNewWorkbookResponse(
            errorReport = er
        )
        proto = o.toProtoObj()
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
            windowId = "abc"
        )
        proto = o.toProtoObj()
        self.assertEqual(o.windowId, proto.windowId)

        o2 = CreateNewWorkbookResponse(
            windowId = None
        )
        proto2 = o2.toProtoObj()
        self.assertFalse(proto2.HasField("windowId"))


if __name__ == '__main__':
    unittest.main()
