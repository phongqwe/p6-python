import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.worksheet.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet


class RpcWorksheet_test(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mockSP = MagicMock()
        mockWsService = MagicMock()
        mockSP.wsService = mockWsService
        self.mockSP = mockSP
        self.mockWsService = mockWsService
        self.ws = RpcWorksheet(
            name = "qwe",
            wbKey = WorkbookKeys.fromNameAndPath("wb1"),
            stubProvider = self.mockSP
        )
    def test_sheetCount(self):
        self.mockWsService.getCellCount = MagicMock(return_value = CellCountResponse(123).toProtoObj())
        self.assertEqual(123, self.ws.size)


if __name__ == '__main__':
    unittest.main()
