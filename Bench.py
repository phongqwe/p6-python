import unittest
from pathlib import Path

from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp

x=123

def zsd():
    return 10

def execz(f):
    print(f())
class Bench(unittest.TestCase):
    def test_z(self):

        d = {
            WorkbookKeyImp("1",Path("11")): 1,
            WorkbookKeyImp("2",Path("22")):2
        }

        ek = WorkbookKeyImp("2",Path("22"))
        print(ek in d.keys())