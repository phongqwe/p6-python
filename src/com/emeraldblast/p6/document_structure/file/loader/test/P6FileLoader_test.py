import os.path
import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoaderStd import P6FileLoaderStd
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok


class P6FileLoader_test(unittest.TestCase):
    def test_something(self):
        loader = P6FileLoaderStd()
        loadRs = loader.loadRs("./file.txt")
        self.assertTrue(isinstance(loadRs,Ok), os.path.abspath(Path("file.txt")))

        loadRs2 = loader.loadRs("not exist file")
        self.assertTrue(isinstance(loadRs2,Err))
        self.assertEqual(loadRs2.err.header, P6FileLoaderErrors.FileNotExist.header)

        loadRs3 = loader.loadRs("malformed_file.txt")
        self.assertTrue(isinstance(loadRs3,Err))
        self.assertEqual(loadRs3.err.header, P6FileLoaderErrors.UnableToReadFile.header)

if __name__ == '__main__':
    unittest.main()
