import threading
import unittest

import zmq

from bicp_document_structure.event.reactor.StdReactorProvider import StdReactorProvider
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.message.SocketProviderImp import SocketProviderImp
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class StdReactorProvider_test(unittest.TestCase):
    def startREPServer(self, isOk, context):
        repSocket = context.socket(zmq.REP)
        repSocket.bind("tcp://*:6000")
        receive = repSocket.recv()
        print(f"Server received: \n{receive}")
        if isOk:
            repSocket.send("ok".encode())
        else:
            repSocket.send("fail".encode())
        repSocket.close()

    def startREPServerOnThread(self, isOk,context) -> threading.Thread:
        thread = threading.Thread(target = self.startREPServer, args = [isOk, context])
        thread.start()
        return thread

    def test_integration_test_default_reactor_ok(self):
        # start mock server
        context = zmq.Context.instance()
        thread = self.startREPServerOnThread(True, context)
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:6000")
        socketProvider = SocketProviderImp(
            reqSocketUI = socket
        )
        def gs():
            return socketProvider
        reactorProvider = StdReactorProvider(gs)
        reactor = reactorProvider.cellUpdateValue()
        def onCellEvent(workbook, worksheet, cell, event):
            reactor.react(CellEventData(
                workbook,worksheet,cell,event
            ))
        wb = EventWorkbook(WorkbookImp("bookz1"),onCellEvent = onCellEvent)
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        cell.value = 123

        # stop mock server
        thread.join()

    def test_integration_test_default_reactor_fail(self):
        # start mock server
        context = zmq.Context.instance()
        thread = self.startREPServerOnThread(False, context)
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:6000")
        socketProvider = SocketProviderImp(reqSocketUI = socket)
        app = AppImp()
        app.initBaseReactor()
        app.socketProvider = socketProvider
        wb = app.createNewWorkbook("bookz1")
        wb.createNewWorksheet("sheetz1")
        cell = app.activeWorkbook.activeWorksheet.cell("@B32")
        with self.assertRaises(Exception):
            cell.value = 123
        thread.join()



if __name__ == '__main__':
    unittest.main()
