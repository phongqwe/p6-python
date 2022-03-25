import threading
import unittest

import zmq

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.proto.DocPM_pb2 import CellProto
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageProto
from bicp_document_structure.message.sender.MessageSender import MessageSender
from bicp_document_structure.util.for_test.TestUtils import findNewSocketPort
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok

# import socket
# sock = socket.socket()
# sock.bind(('', 0))
# port = sock.getsockname()[1]
# sock.close()
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
    messageObj = P6Message(
        header = P6MessageHeader("id1", P6Events.Cell.UpdateValueEvent),
        content = CellJson(
            value = "cell value",
            script = "cell script",
            formula = "=1234",
            address = CellAddressJson(1, 34)
        )
    )

    def test_sendOk(self):
        context = zmq.Context.instance()
        thread = threading.Thread(target = startREPServer, args = [True, context])
        thread.start()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        reply = MessageSender.sendREQ(socket, MessageSenderREQTest.messageObj)
        self.assertTrue(isinstance(reply, Ok))
        socket.close()
        thread.join()

    def test_sendFail(self):
        context = zmq.Context.instance()
        thread = threading.Thread(target = startREPServer, args = [False, context])
        thread.start()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        reply = MessageSender.sendREQ(socket, MessageSenderREQTest.messageObj)
        self.assertTrue(isinstance(reply, Err))
        socket.close()
        thread.join()

    messageForProto = P6Message(
        header = P6MessageHeader("id1", P6Events.Cell.UpdateValueEvent),
        content = DataCell(
            value = "cell value",
            script = "cell script",
            formula = "=1234",
            address = CellIndex(1, 34)
        )
    )

    def test_sendProtoOk(self):
        def onReceive(data):
            proto = P6MessageProto()
            proto.ParseFromString(data)
            print("receive proto:")
            print(proto)
            dataRaw = proto.data
            data = CellProto()
            data.ParseFromString(bytes(dataRaw,"utf-8"))
            print("*data:")
            print(data)

        context = zmq.Context.instance()
        thread = threading.Thread(target = startREPServerProto, args = [True, context,onReceive])
        thread.start()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        reply = MessageSender.sendREQ_Proto(socket, MessageSenderREQTest.messageForProto)
        self.assertTrue(isinstance(reply, Ok))
        socket.close()
        thread.join()