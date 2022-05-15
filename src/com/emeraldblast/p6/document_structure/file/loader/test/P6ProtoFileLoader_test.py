import os
import unittest
from pathlib import Path

from com.emeraldblast.p6.document_structure.file.saver.P6ProtoFileSaver import P6ProtoFileSaver

from com.emeraldblast.p6.document_structure.file.loader.P6ProtoFileLoader import P6ProtoFileLoader
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleWb, compareWs

from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


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
        self.assertEqual(workbook.worksheetCount, lwb.worksheetCount)
        for x in range(workbook.worksheetCount):
            self.assertTrue(compareWs(workbook.getWorksheet(x),lwb.getWorksheet(x)))

        os.remove(path)


if __name__ == '__main__':
    unittest.main()
