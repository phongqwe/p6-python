import threading

import zmq
from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6MessageProto

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactors import EventReactors
from com.emeraldblast.p6.document_structure.communication.reactor.MutableEventReactorContainer import \
    MutableEventReactorContainer
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import findNewSocketPort


class NotificationListener:

    def __init__(self,zContext):
        self.port=None
        self.zContext=zContext
        self.senderSocket = None
        self.receivingSocket = None
        self.thread = None
        self.reactorContainer:EventReactorContainer = MutableEventReactorContainer()

        # def defaultReactorCB(data):
        #     print(f"{data}")

        # defaultReactor = EventReactors.makeBasicReactor(defaultReactorCB)
        #
        # for event in P6Events.Cell.allEvents():
        #     self.reactorContainer.addReactor(event, defaultReactor)
        # for event in P6Events.Workbook.allEvents():
        #     self.reactorContainer.addReactor(event, defaultReactor)
        # for event in P6Events.Worksheet.allEvents():
        #     self.reactorContainer.addReactor(event, defaultReactor)
        # for event in P6Events.App.allEvents():
        #     self.reactorContainer.addReactor(event, defaultReactor)


    def onReceive(self,data:bytes):
        # msg = P6MessageProto()
        # msg.ParseFromString(data)
        # print(msg)
        p6Res = P6Response.fromProtoByte(data)
        self.reactorContainer.triggerReactorsFor(p6Res.header.eventType, p6Res.data)

    def addReactor(self,event:P6Event,reactor:EventReactor):
        self.reactorContainer.addReactor(event,reactor)


    def start(self):
        while True:
            receive = self.receivingSocket.recv()
            self.receivingSocket.send(b"ok")
            if receive == b"close":
                break
            self.onReceive(receive)
        if self.receivingSocket:
            self.receivingSocket.close()
            self.receivingSocket = None

    def startOnThread(self):
        self.port = findNewSocketPort()
        self.receivingSocket = self.zContext.socket(zmq.REP)
        self.receivingSocket.bind(f"tcp://*:{self.port}")
        self.senderSocket = self.zContext.socket(zmq.REQ)
        self.senderSocket.connect(f"tcp://localhost:{self.port}")

        self.thread = threading.Thread(target = self.start)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.senderSocket.send(b"close")
        rec = self.senderSocket.recv()
        if self.senderSocket:
            self.senderSocket.close()
            self.senderSocket = None

        if self.receivingSocket:
            self.receivingSocket.close()
            self.receivingSocket = None

        if self.thread is not None:
            self.thread.join()
            self.thread = None