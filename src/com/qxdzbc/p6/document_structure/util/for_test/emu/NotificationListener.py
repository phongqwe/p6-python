import threading
from typing import Callable

import zmq

from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import findNewSocketPort
from com.qxdzbc.p6.new_architecture.communication import EventReactor
from com.qxdzbc.p6.new_architecture.communication import EventReactorContainer
from com.qxdzbc.p6.new_architecture.communication import EventReactors
from com.qxdzbc.p6.new_architecture.communication import \
    MutableEventReactorContainer
from com.qxdzbc.p6.new_architecture.communication import P6Event
from com.qxdzbc.p6.new_architecture.communication import P6Events
from com.qxdzbc.p6.new_architecture.communication.response import P6Response


class NotificationListener:

    def __init__(self,zContext):
        self.port=None
        self.zContext=zContext
        self.senderSocket = None
        self.receivingSocket = None
        self.thread = None
        self.reactorContainer:EventReactorContainer = MutableEventReactorContainer()


    def onReceive(self,data:bytes):
        p6Res = P6Response.fromProtoBytes(data)
        self.reactorContainer.triggerReactorsFor(p6Res.header.eventType, p6Res.data)

    def addReactor(self,event:P6Event,reactor:EventReactor):
        self.reactorContainer.addReactor(event,reactor)

    def addReactorCB(self,event:P6Event, reactorCB:Callable[[bytes],None]):
        reactor = EventReactors.makeBasicReactor(reactorCB)
        self.addReactor(event,reactor)

    def addAllEventReactor(self,reactor):
        for event in P6Events.Cell.allEvents():
            self.reactorContainer.addReactor(event, reactor)
        for event in P6Events.Workbook.allEvents():
            self.reactorContainer.addReactor(event, reactor)
        for event in P6Events.Worksheet.allEvents():
            self.reactorContainer.addReactor(event, reactor)
        for event in P6Events.App.allEvents():
            self.reactorContainer.addReactor(event, reactor)

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