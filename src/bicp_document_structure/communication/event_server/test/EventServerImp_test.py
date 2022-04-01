import unittest
from typing import Any

import zmq

from bicp_document_structure.communication.event_server.msg.P6Message import P6Message
from bicp_document_structure.communication.event_server.response.P6Response import P6Response
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.EventReactor import EventReactor
from bicp_document_structure.communication.proto.CommonProtos_pb2 import ErrorReportProto
from bicp_document_structure.communication.proto.P6MsgProtos_pb2 import P6ResponseProto
from bicp_document_structure.communication.event_server.EventServerErrors import EventServerErrors
from bicp_document_structure.communication.event_server.EventServerImp import EventServerImp
from bicp_document_structure.util.CommonError import CommonErrors
from bicp_document_structure.util.for_test.TestUtils import findNewSocketPort, MockToProto


class MockReactor(EventReactor[Any, None]):
    def __init__(self, cb):
        self.cb = cb

    @property
    def id(self) -> str:
        return "id"

    def react(self, data: Any) -> None:
        return self.cb(data)


class EventServerImp_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.port = findNewSocketPort()
        port = self.port
        self.sv = EventServerImp(True)
        self.socket = zmq.Context.instance().socket(zmq.REQ)
        self.socket.connect(f"tcp://localhost:{port}")
        self.x = None
        self.sv.start(port)

    def tearDown(self) -> None:
        super().tearDown()
        self.sv.stop()
        self.socket.close()

    def test_malformed_msg(self):
        socket = self.socket
        socket.send(bytes("z", "utf-8"))
        o = socket.recv()
        print(o)

    def test_handleOk(self):
        sv = self.sv
        socket = self.socket

        def cb(dt):
            self.x = 1
            return MockToProto(dt.data)

        mockReactor = MockReactor(cb)
        sv.addReactor(P6Events.Worksheet.Rename.event, mockReactor)
        socket.send(
            P6Message.create(P6Events.Worksheet.Rename.event, b"abc").toProtoBytes()
        )
        o = socket.recv()
        self.assertEqual(1, self.x)

    def test_handle_noHandler(self):
        sv = self.sv
        socket = self.socket

        def cb(dt):
            self.x = 1
            return MockToProto(dt.data)

        mockReactor = MockReactor(cb)
        sv.addReactor(P6Events.Workbook.CreateNewWorksheet.event, mockReactor)
        request = P6Message.create(P6Events.Worksheet.Rename.event, b"abc")
        socket.send(request.toProtoBytes())
        o = socket.recv()
        resProto = P6ResponseProto()
        resProto.ParseFromString(o)
        print(resProto)
        res = P6Response.fromProto(resProto)
        self.assertEqual(P6Response.Status.ERROR, res.status)
        self.assertEqual(request.header, res.header)
        errReportProto = ErrorReportProto()
        errReportProto.ParseFromString(res.data)
        self.assertEqual(EventServerErrors.NoReactorReport.header.errorCode, errReportProto.errorCode)
        self.assertEqual(None, self.x)

    def test_handle_CatchAll(self):
        sv = self.sv
        socket = self.socket

        def cb(dt):
            raise Exception("x")

        mockReactor = MockReactor(cb)
        sv.addReactor(P6Events.Worksheet.Rename.event, mockReactor)
        input = P6Message.create(P6Events.Worksheet.Rename.event, b"abc")
        socket.send(input.toProtoBytes())
        o = socket.recv()
        resProto = P6ResponseProto()
        resProto.ParseFromString(o)
        res = P6Response.fromProto(resProto)
        self.assertEqual(P6Response.Status.ERROR, res.status)
        self.assertNotEqual(input.header, res.header)
        errReportProto = ErrorReportProto()
        errReportProto.ParseFromString(res.data)
        self.assertEqual(CommonErrors.ExceptionErrorReport.header.errorCode, errReportProto.errorCode)


if __name__ == '__main__':
    unittest.main()
