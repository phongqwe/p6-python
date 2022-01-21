import unittest

from bicp_document_structure.cell.cache.DataCacheImp import DataCacheImp


class DataCacheImpTest(unittest.TestCase):
    def test_all(self):
        cache = DataCacheImp(123)
        self.assertTrue(cache.hasValue())
        self.assertEqual(123,cache.value)
        cache.clear()
        self.assertFalse(cache.hasValue())

        cache.value = "new value"
        self.assertEqual("new value",cache.value)
        self.assertTrue(cache.hasValue())




if __name__ == '__main__':
    unittest.main()
