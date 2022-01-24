import os.path
import unittest
from pathlib import Path

from bicp_document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from bicp_document_structure.file.loader.P6FileLoaderStd import P6FileLoaderStd
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok


class P6FileLoader_test(unittest.TestCase):
    def test_something(self):
        loader = P6FileLoaderStd()
        loadRs = loader.load("./file.txt")
        self.assertTrue(isinstance(loadRs,Ok),os.path.abspath(Path("./file.txt")))

        loadRs2 = loader.load("not exist file")
        self.assertTrue(isinstance(loadRs2,Err))
        self.assertEqual(loadRs2.err.header, P6FileLoaderErrors.FileNotExist.header)

        loadRs3 = loader.load("malformed_file.txt")
        self.assertTrue(isinstance(loadRs3,Err))
        self.assertEqual(loadRs3.err.header, P6FileLoaderErrors.UnableToReadFile.header)

if __name__ == '__main__':
    unittest.main()
