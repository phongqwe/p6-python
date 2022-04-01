import unittest

from bicp_document_structure.communication.P6MessageHeader import P6MessageHeader
from bicp_document_structure.communication.event_server.response.P6Response import P6Response
from bicp_document_structure.communication.event.P6Events import P6Events


class P6Response_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.r = P6Response(
            header = P6MessageHeader("id", P6Events.Cell.UpdateValue.event),
            data = b"data 123",
            status = P6Response.Status.OK
        )

    def test_toProto(self):
        proto = self.r.toProtoObj()


if __name__ == '__main__':
    unittest.main()
