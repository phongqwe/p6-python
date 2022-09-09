import threading
import unittest

import zmq

from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import findNewSocketPort
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.communication.msg.P6MessageHeader import P6MessageHeader
from com.qxdzbc.p6.new_architecture.communication.msg.P6Events import P6Events
from com.qxdzbc.p6.new_architecture.communication.msg.P6Message import P6Message
from com.qxdzbc.p6.new_architecture.communication.sender.MessageSender import MessageSender
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto
from com.qxdzbc.p6.proto.P6MsgProtos_pb2 import P6MessageProto

port = findNewSocketPort()


def startREPServer(isOk, context):
    repSocket = context.socket(zmq.REP)
    repSocket.bind(f"tcp://*:{port}")
    receive = repSocket.recv()
    print(f"Server received: \n{receive}")
    if isOk:
        repSocket.send("ok".encode())
    else:
        repSocket.send("fail".encode())
    repSocket.close()


def startREPServerProto(isOk, context, onReceive):
    repSocket = context.socket(zmq.REP)
    repSocket.bind(f"tcp://*:{port}")
    receive = repSocket.recv()
    onReceive(receive)
    if isOk:
        repSocket.send("ok".encode())
    else:
        repSocket.send("fail".encode())
    repSocket.close()


class MessageSenderREQTest(unittest.TestCase):
    messageForProto = P6Message(
        header = P6MessageHeader("id1", P6Events.Cell.Update.event),
        data = DataCell(
            value = "cell value",
            formula = "=1234",
            address = CellIndex(1, 34),
            wsName = "ws1",
            wbKey = WorkbookKeys.fromNameAndPath("wb")
        )
    )

    def test_sendProtoOk(self):
        def onReceive(data):
            proto = P6MessageProto()
            proto.ParseFromString(data)
            print("receive proto:")
            print(proto)
            data = CellProto()
            data.ParseFromString(proto.data)
            print("*data:")
            print(data)

        context = zmq.Context.instance()
        thread = threading.Thread(target = startREPServerProto, args = [True, context, onReceive])
        thread.start()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        reply = MessageSender.sendREQ_Proto(socket, MessageSenderREQTest.messageForProto)
        self.assertTrue(reply.isOk())
        socket.close()
        thread.join()
