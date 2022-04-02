import unittest
from unittest.mock import MagicMock

import zmq
from bicp_document_structure.communication.proto.CellProtos_pb2 import CellUpdateCommonResponseProto

from bicp_document_structure.communication.proto.P6MsgProtos_pb2 import P6ResponseProto

from bicp_document_structure.communication.proto.DocProtos_pb2 import WorkbookProto

from bicp_document_structure.communication.SocketProviderImp import SocketProviderImp
from bicp_document_structure.communication.event.reactor.StdReactorProvider import StdReactorProvider
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.util.for_test.TestUtils import findNewSocketPort, startREPServerOnThread, sendClose
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp

port = findNewSocketPort()


class StdReactorProvider_test(unittest.TestCase):

    def onReceive(self, data):
        print(data)

    def tearDown(self) -> None:
        sendClose(self.socket)
        self.socket.close()
        self.thread.join()
        # self.context.destroy()

    def setUp(self) -> None:
        super().setUp()
        self.context = zmq.Context.instance()
        context = self.context
        port = findNewSocketPort()
        self.thread = startREPServerOnThread(True, port, context, self.onReceive)
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://localhost:{port}")
        socketProvider = SocketProviderImp(reqSocketUI = self.socket)
        def gs():
            return socketProvider
        self. reactorProvider = StdReactorProvider(gs)



    def test_cellUpdateReactor(self):
        self.sentObj = 123
        self.receiveObj = 234

        port = findNewSocketPort()
        def onReceive(data):
            p6Res = P6ResponseProto()
            p6Res.ParseFromString(data)
            receive = CellUpdateCommonResponseProto()
            receive.ParseFromString(p6Res.data)
            self.receiveObj = receive

        thread = startREPServerOnThread(True, port, self.context, onReceive)
        socket = self.context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        socketProvider = SocketProviderImp(reqSocketUI = socket)

        def gs():
            return socketProvider

        self.reactorProvider = StdReactorProvider(gs)
        reactor = self.reactorProvider.cellUpdateReactor()

        def onCellEvent(data: CellEventData):
            reactor.react(data)
            self.sentObj = data.data.toProtoObj()

        wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent)
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        cell.value = 123
        socket.send(b"close")
        socket.close()
        thread.join()
        self.assertEqual(self.sentObj, self.receiveObj)
        print(self.sentObj)


    def test_integration_test_default_reactor_ok(self):
            # start mock server
            reactor = self.reactorProvider.cellUpdateReactor()

            def onCellEvent(data:CellEventData):
                reactor.react(data)

            wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent, onWorkbookEvent = MagicMock())
            wb.createNewWorksheet("sheetz1")
            cell = wb.activeWorksheet.cell("@B32")
            cell.value = 123

    def test_integration_test_default_reactor_fail(self):
        """ why should there be an exception? """
        reactor = self.reactorProvider.cellUpdateReactor()

        def onCellEvent(data:CellEventData):
            reactor.react(data)

        wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent)
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        # with self.assertRaises(Exception):
        #     cell.value = 123


if __name__ == '__main__':
    unittest.main()
