import unittest

from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.IndWorksheet import IndWorksheet
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId


class IndWorksheet_test(unittest.TestCase):
    def test_ToProto(self):
        o = IndWorksheet(
            id = WorksheetId(
                wbKey=WorkbookKeys.fromNameAndPath("wb"),
                wsName = "ws1"
            ),
            cells = [
                IndCell(CellAddresses.fromLabel("B3"),CellValue.fromNum(123)),
                IndCell(CellAddresses.fromLabel("C10"),formula = "qqq"),
            ]
        )
        p = o.toProtoObj()
        self.assertEqual(o.id.toProtoObj(),p.id)
        expectedCells = list(map(lambda c: c.toProtoObj(), o.cells))
        self.assertEqual(expectedCells,list(p.cells))


if __name__ == '__main__':
    unittest.main()
