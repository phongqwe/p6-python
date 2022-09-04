import unittest
from pathlib import Path

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCellResponse import \
    DeleteCellResponse
from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class DeleteCellResponse_test(unittest.TestCase):
    def test_something(self):
        o = DeleteCellResponse(
            workbookKey = WorkbookKeys.fromNameAndPath("AAA",Path("qwe").absolute()),
            worksheetName = "WS123",
            cellAddress = CellAddresses.fromRowCol(123,321),
            workbook = WorkbookImp("zxc"),
            isError = True,
            errorReport = ErrorReport(
                header=ErrorHeader("ecode123","qweqweqwe")
            )
        )
        proto = o.toProtoObj()
        self.assertEqual(o.newWorkbook.toProtoObj(), proto.newWorkbook)
        self.assertEqual(o.workbookKey.toProtoObj(),proto.workbookKey)
        self.assertEqual(o.worksheetName,proto.worksheetName)
        self.assertEqual(o.isError,proto.isError)
        self.assertEqual(o.errorReport.toProtoObj(),proto.errorReport)


if __name__ == '__main__':
    unittest.main()
