import unittest

from bicp_document_structure.message.MsgType import MsgType


class Bench(unittest.TestCase):
    def test_z(self):
        print(MsgType.CELL_VALUE_EDIT.value)
