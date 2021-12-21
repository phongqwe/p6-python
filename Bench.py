import json
import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.address.CellLabel import CellLabel
from bicp_document_structure.column.ColumnImp import ColumnImp

x=123

def zsd():
    return 10
class Bench(unittest.TestCase):
    def test_z(self):
        c = CellIndex(1,1)
        cell = DataCell(c,123,"")
        j = cell.toJson()
        print(json.dumps(cell.toJson().__dict__))

        col = ColumnImp.empty(1)
        col.addCell(cell)
        col.addCell(DataCell(CellLabel("@A2"),456,""))

        colJson = json.dumps(col.toJson().__dict__)
        print(colJson)



