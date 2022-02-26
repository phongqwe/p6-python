import unittest

from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd=P6MessageHeader("id1", MsgType.CellUpdateValue)
        print(hd.toJsonStr())
        self.assertEqual("""{"msgId": "id1", "msgType": "cell_value_update"}""",hd.toJsonStr())
