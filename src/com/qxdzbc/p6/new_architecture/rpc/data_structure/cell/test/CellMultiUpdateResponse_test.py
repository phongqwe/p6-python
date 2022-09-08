import unittest

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.communication import P6EventTableImp
from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell.CellMultiUpdateResponse import \
    CellMultiUpdateResponse


class CellMultiUpdateResponse_test(unittest.TestCase):
    def test_toEventData(self):
        o =CellMultiUpdateResponse(
            isError = False,
            workbookKey = WorkbookKeys.fromNameAndPath("B"),
            errorReport = None,
            newWorkbook = None
        )
        edt = o.toEventData()
        self.assertEqual(P6EventTableImp.i().getEventForClazz(CellMultiUpdateResponse),edt.event)
        self.assertEqual(o,edt.data)



if __name__ == '__main__':
    unittest.main()
