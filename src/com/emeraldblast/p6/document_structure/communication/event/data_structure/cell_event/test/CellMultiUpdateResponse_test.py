import unittest

from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp

from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateResponse import \
    CellMultiUpdateResponse
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


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