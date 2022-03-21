import threading
import unittest

import zmq

from bicp_document_structure.event.reactor.StdReactorProvider import StdReactorProvider
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.message.SocketProviderImp import SocketProviderImp
from bicp_document_structure.util.for_test.TestUtils import findNewSocketPort
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp

port = findNewSocketPort()


class StdReactorProvider_test(unittest.TestCase):
    def startREPServer(self, isOk, context):
        repSocket = context.socket(zmq.REP)
        repSocket.bind(f"tcp://*:{port}")
        receive = repSocket.recv()
        print(f"Server received: \n{receive}")
        if isOk:
            repSocket.send("ok".encode())
        else:
            repSocket.send("fail".encode())
        repSocket.close()

    def startREPServerOnThread(self, isOk, zContext) -> threading.Thread:
        thread = threading.Thread(target = self.startREPServer, args = [isOk, zContext])
        thread.start()
        return thread

    # def z(self):
    #     context = zmq.Context.instance()
    #     socket = context.socket(zmq.REQ)
    #     socket.connect("tcp://localhost:6000")
    #     getApp().socketProvider.updateREQSocketForUIUpdating(socket)

    def test_integration_test_default_reactor_ok(self):
        # start mock server
        context = zmq.Context.instance()
        thread = self.startREPServerOnThread(True, context)
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        socketProvider = SocketProviderImp(reqSocketUI = socket)

        def gs():
            return socketProvider

        reactorProvider = StdReactorProvider(gs)
        reactor = reactorProvider.cellUpdateValue()

        def onCellEvent(workbook, worksheet, cell, event):
            reactor.react(CellEventData(
                workbook, worksheet, cell, event
            ))

        wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent)
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        cell.value = 123

        # stop mock server
        thread.join()
        context.destroy()

    def test_integration_test_default_reactor_fail(self):
        # start mock server
        context = zmq.Context.instance()

        thread = self.startREPServerOnThread(isOk = False, zContext = context)
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        socketProvider = SocketProviderImp(reqSocketUI = socket)

        def gs():
            return socketProvider

        reactorProvider = StdReactorProvider(gs)
        reactor = reactorProvider.cellUpdateValue()

        def onCellEvent(workbook, worksheet, cell, event):
            reactor.react(CellEventData(
                workbook, worksheet, cell, event
            ))

        wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent)
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        with self.assertRaises(Exception):
            cell.value = 123
        thread.join()
        context.destroy()


if __name__ == '__main__':
    unittest.main()
