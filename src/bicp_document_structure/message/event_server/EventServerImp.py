import threading

import zmq

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6Response import P6Response
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.event.reactor.EventReactor import EventReactor
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageProto
from bicp_document_structure.message.event_server.EventServer import EventServer
from bicp_document_structure.message.event_server.EventServerErrors import EventServerErrors
from bicp_document_structure.util.CommonError import CommonErrors
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport


def startRenameServer():
    server = EventServerImp()
    server.start()
    return server


class EventServerImp(EventServer):

    def __init__(self, port: int, isDaemon:bool = True):
        self._port = port
        self._isRunning = False
        self._thread = None
        self._reactorDict: dict[P6Event, EventReactor[P6Message,ToProto]] = {}
        self._isDaemon = isDaemon
        zContext = zmq.Context.instance()
        self._socket = zContext.socket(zmq.REP)
        self._socket.bind(f"tcp://*:{self._port}")

    def start(self):
        self._isRunning = True
        repSocket = self._socket
        def daemonRun():
            while self._isRunning:
                recv = repSocket.recv()
                try: # try to catch all exceptions to prevent this server from crashing
                    p6MsgProto = P6MessageProto()
                    p6MsgProto.ParseFromString(recv)
                    p6Msg: P6Message = P6Message.fromProto(p6MsgProto)
                    reactor: EventReactor[P6Message, ToProto] | None = self.getReactorsForEvent(p6Msg.header.eventType)
                    if reactor is not None:
                        # no reactor for the request event -> return error
                        outputBytes:bytes = reactor.react(p6Msg).toProtoBytes()
                        p6Res = P6Response(
                            header = p6Msg.header,
                            data = outputBytes,
                            status = P6Response.Status.OK)
                        repSocket.send(p6Res.toProtoBytes())
                    else:
                        # has reactor -> return reactor result
                        p6Res = P6Response(
                            header = p6Msg.header,
                            data = EventServerErrors.NoReactorReport(p6Msg.header.eventType),
                            status = P6Response.Status.ERROR
                        )
                        repSocket.send(p6Res.toProtoBytes())
                except Exception as e:
                    # catch-all response
                    p6Res:P6Response = P6Response.create(
                        event = P6Events.EventServer.Unknown,
                        data = CommonErrors.ExceptionErrorReport(e),
                        status = P6Response.Status.ERROR)
                    repSocket.send(p6Res.toProtoBytes())

        # the main logic runs a blocking operation, so I keep it in a daemon thread so that I can kill the main logic by killing its parent thread which does not have any blocking operation
        def run():
            daemonThread = threading.Thread(target = daemonRun)
            daemonThread.daemon = True
            daemonThread.start()
            while self._isRunning:
                pass

        self._thread = threading.Thread(target = run)
        self._thread.daemon = self._isDaemon
        self._thread.start()

    def stop(self):
        self._isRunning = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        # if self._socket is not None:
        #     self._socket.close()
        #     self._socket = None

    def getReactorsForEvent(self, event: P6Event) -> EventReactor[P6Message, ToProto] | None:
        return self._reactorDict.get(event)

    def addReactor(self, event: P6Event, reactor: EventReactor[P6Message, ToProto]):
        self._reactorDict[event] = reactor

    def removeReactorsForEvent(self, event: P6Event):
        if event in self._reactorDict.keys():
            self._reactorDict.pop(event)

    def isEmpty(self) -> bool:
        return len(self._reactorDict) == 0
