import unittest

from com.qxdzbc.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp

from com.qxdzbc.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateResponse import \
    CellUpdateResponse
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class CellUpdateResponse_test(unittest.TestCase):
    def test_toEventData(self):
        o = CellUpdateResponse(
            isError = False,
            workbookKey = WorkbookKeys.fromNameAndPath("B"),
            errorReport = None,
            newWorkbook = None
        )
        edt = o.toEventData()
        self.assertEqual(P6EventTableImp.i().getEventForClazz(CellUpdateResponse), edt.event)
        self.assertEqual(o, edt.data)


if __name__ == '__main__':
    unittest.main()
