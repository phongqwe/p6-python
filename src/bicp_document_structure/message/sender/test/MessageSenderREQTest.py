import threading
import unittest

import zmq

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.sender.MessageSenderREQ import MessageSenderREQ
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok


def startREPServer(isOk, context):
    repSocket = context.socket(zmq.REP)
    repSocket.bind("tcp://*:6000")
    receive = repSocket.recv()
    print(f"Server received: \n{receive}")
    if isOk:
        repSocket.send("ok".encode())
    else:
        repSocket.send("fail".encode())
    repSocket.close()


class MessageSenderREQTest(unittest.TestCase):
    messageObj = P6Message(
        header = P6MessageHeader("id1", MsgType.CELL_VALUE_EDIT),
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
        socket.connect("tcp://localhost:6000")
        sender = MessageSenderREQ(socket)
        reply = sender.send(MessageSenderREQTest.messageObj)
        self.assertTrue(isinstance(reply, Ok))
        socket.close()
        thread.join()

    def test_sendFail(self):
        context = zmq.Context.instance()
        thread = threading.Thread(target = startREPServer, args = [False, context])
        thread.start()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:6000")
        sender = MessageSenderREQ(socket)
        reply = sender.send(MessageSenderREQTest.messageObj)
        self.assertTrue(isinstance(reply, Err))
        socket.close()
        thread.join()