import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.proto.DocProtos_pb2 import WorksheetProto, CellProto

from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson
from com.emeraldblast.p6.document_structure.worksheet.Worksheets import Worksheets


class Worksheets_test(unittest.TestCase):

    def test_FromProto(self):
        wsProto = WorksheetProto()
        wsProto.name = "Sheet1"

        a1 = CellProto()
        a1.address.CopyFrom(CellAddresses.fromLabel("@A1").toProtoObj())
        a1.value = "123"

        x12Proto = CellProto()

        x12Proto.address.CopyFrom(CellAddresses.fromLabel("@X12").toProtoObj())
        x12Proto.value = "a string"
        x12Proto.formula = "formula x12"

        wsProto.cell.extend([
            a1, x12Proto
        ])

        ws: Worksheet = Worksheets.fromProto(wsProto, MagicMock())
        self.assertEqual(wsProto.name, ws.name)
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@A1")))
        self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("@X12")))
        self.assertEqual(2, len(ws.cells))
        self.assertEqual(ws, ws.cell("@A1").worksheet)
        self.assertEqual(ws, ws.cell("@X12").worksheet)


    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def test_something(self):
        json = WorksheetJson(
            name = "sheet1",
            cells = [
                CellJson("value1", "script1", "formula1", CellAddressJson(1, 2)),
                CellJson("value2", "script2", "formula2", CellAddressJson(2, 3)),
                CellJson("value3", "script3", "formula3", CellAddressJson(3, 4))
            ]
        )
        sheet = Worksheets.wsFromJson(json, workbook = MagicMock())
        self.assertTrue(isinstance(sheet, Worksheet))
        self.assertEqual(json.name, sheet.name)
        # cell12 = sheet.cell((1,2))
        # self.assertEqual()


if __name__ == '__main__':
    unittest.main()
