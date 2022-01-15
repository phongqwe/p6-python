import unittest

from bicp_document_structure.cell.CacheCell import CacheCell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.cache.DataCacheImp import DataCacheImp


class CacheCellTest(unittest.TestCase):
    def test_getValue(self):
        cache = DataCacheImp()
        self.executionCounter = 0

        def z(cd,ce):
            self.executionCounter+=1
            return None

        cacheCell = CacheCell(
            cell=DataCell(
                address=CellIndex(1, 1),
                code="x=100;x+1", onCellMutation=z
            ),
            cache=cache
        )
        # run the script
        self.assertEqual(101, cacheCell.value)
        self.assertTrue(cache.isNotEmpty())
        self.assertEqual(101,cache.value)
        # run the script again
        cacheCell.value
        self.assertEqual(1,self.executionCounter)
        self.assertEqual(101, cache.value)
        # new script and run
        cacheCell.setScriptAndRun("x=1;x+20")
        self.assertEqual(21,cache.value)
        self.assertEqual(3,self.executionCounter)

        # just new script
        cacheCell.script = "123"
        self.assertTrue(cache.isEmpty())
