import unittest


class WorkbookUpdateCommonResponse_test(unittest.TestCase):
    pass
    # def test_toProtoObj_1(self):
    #     o = WorkbookUpdateCommonResponse(
    #         isError = False,
    #         workbookKey = WorkbookKeys.fromNameAndPath("b1",None),
    #         newWorkbook = WorkbookImp("B1")
    #     )
    #     proto = o.toProtoObj()
    #     self.assertEqual(o.workbookKey.toProtoObj(), proto.workbookKey)
    #     self.assertEqual(o.newWorkbook.toProtoObj(), proto.newWorkbook)
    #     self.assertFalse(proto.isError)
    #     self.assertFalse(proto.HasField("errorReport"))
    #
    # def test_toProtoObj_2(self):
    #     o = WorkbookUpdateCommonResponse(
    #         workbookKey = WorkbookKeys.fromNameAndPath("b1",None),
    #         newWorkbook = WorkbookImp("B1"),
    #         isError = True,
    #         errorReport = ErrorReport(
    #             header=ErrorHeader("errCode","Description"),
    #             data = None
    #         )
    #     )
    #     proto = o.toProtoObj()
    #     self.assertEqual(o.workbookKey.toProtoObj(), proto.workbookKey)
    #     self.assertEqual(o.newWorkbook.toProtoObj(), proto.newWorkbook)
    #     self.assertTrue(proto.isError)
    #     self.assertEqual(o.errorReport.toProtoObj(),proto.errorReport)

if __name__ == '__main__':
    unittest.main()
