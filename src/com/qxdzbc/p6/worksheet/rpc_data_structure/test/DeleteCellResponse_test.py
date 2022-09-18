import unittest


class DeleteCellResponse_test(unittest.TestCase):
    pass
    # def test_something(self):
    #     o = DeleteCellResponse(
    #         workbookKey = WorkbookKeys.fromNameAndPath("AAA",Path("qwe").absolute()),
    #         worksheetName = "WS123",
    #         cellAddress = CellAddresses.fromRowCol(123,321),
    #         workbook = WorkbookImp("zxc"),
    #         isError = True,
    #         errorReport = ErrorReport(
    #             header=ErrorHeader("ecode123","qweqweqwe")
    #         )
    #     )
    #     proto = o.toProtoObj()
    #     self.assertEqual(o.newWorkbook.toProtoObj(), proto.newWorkbook)
    #     self.assertEqual(o.workbookKey.toProtoObj(),proto.workbookKey)
    #     self.assertEqual(o.worksheetName,proto.worksheetName)
    #     self.assertEqual(o.isError,proto.isError)
    #     self.assertEqual(o.errorReport.toProtoObj(),proto.errorReport)


if __name__ == '__main__':
    unittest.main()
