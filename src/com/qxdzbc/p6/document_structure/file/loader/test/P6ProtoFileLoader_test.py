import os
import unittest
from pathlib import Path

from com.qxdzbc.p6.document_structure.file.loader.P6ProtoFileLoader import P6ProtoFileLoader
from com.qxdzbc.p6.document_structure.file.saver.P6ProtoFileSaver import P6ProtoFileSaver
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import sampleWb, compareWs


class P6ProtoFileLoader_test(unittest.TestCase):

    def test_loadRs(self):
        fileName = "fileProto1.txt"
        path = Path(fileName)
        workbook = sampleWb("Book1")
        loader = P6ProtoFileLoader()
        saver = P6ProtoFileSaver()
        saver.saveRs(workbook,path)

        loadWbRs = loader.loadRs(path)
        self.assertTrue(loadWbRs.isOk())
        lwb = loadWbRs.value
        self.assertEqual(fileName, lwb.workbookKey.fileName)
        self.assertEqual(path, lwb.workbookKey.filePath)
        self.assertEqual(workbook.sheetCount, lwb.sheetCount)
        for x in range(workbook.sheetCount):
            self.assertTrue(compareWs(workbook.getWorksheet(x),lwb.getWorksheet(x)))

        os.remove(path)


if __name__ == '__main__':
    unittest.main()