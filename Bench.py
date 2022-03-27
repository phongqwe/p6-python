import unittest

from bicp_document_structure.message.proto.WorkbookProto_pb2 import CreateNewWorksheetProto


class Bench(unittest.TestCase):

    def f1(self,x,y):

        return x+y
    def test_z(self):
        z = CreateNewWorksheetProto()


