import unittest

from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd=P6MessageHeader("id1", P6Events.Cell.UpdateValue)
        print(hd.toJsonStr())
        self.assertEqual("""{"msgId": "id1", "msgType": "cell_value_update"}""",hd.toJsonStr())
