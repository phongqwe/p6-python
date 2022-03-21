import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader


class P6MessageTest(unittest.TestCase):
    def test_toRawMsg(self):
        contentObj = CellJson(
            value="cell value",
            script="cell script",
            formula="=1234",
            address=CellAddressJson(1, 34)
        )
        hd = P6MessageHeader("id1", P6Events.Cell.UpdateValue)
        msg = P6Message(
            header=hd,
            content=contentObj
        )
        jsonStr = msg.toJsonStr()
        expectaction = """{"header": {"msgId": "id1", "msgType": "cell_value_update"}, "content": {"data": "{\\\"value\\\": \\\"cell value\\\", \\\"script\\\": \\\"cell script\\\", \\\"formula\\\": \\\"=1234\\\", \\\"address\\\": {\\\"row\\\": 34, \\\"col\\\": 1}}"}}"""
        self.assertEqual(expectaction, jsonStr)
        self.assertEqual(bytes(expectaction.encode("UTF-8")),msg.toBytes())
