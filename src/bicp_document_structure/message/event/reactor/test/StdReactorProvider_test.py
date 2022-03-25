import unittest
from unittest.mock import MagicMock

import zmq

from bicp_document_structure.message.SocketProviderImp import SocketProviderImp
from bicp_document_structure.message.event.reactor.StdReactorProvider import StdReactorProvider
from bicp_document_structure.message.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.util.for_test.TestUtils import findNewSocketPort, startREPServerOnThread, sendClose
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp

port = findNewSocketPort()


class StdReactorProvider_test(unittest.TestCase):

    def onReceive(self, data):
        print(data)

    def test_integration_test_default_reactor_ok(self):
        # start mock server
        context = zmq.Context.instance()
        port = findNewSocketPort()
        thread = startREPServerOnThread(True, port, context, self.onReceive)
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

        wb = EventWorkbook(WorkbookImp("bookz1"), onCellEvent = onCellEvent, onWorkbookEvent = MagicMock())
        wb.createNewWorksheet("sheetz1")
        cell = wb.activeWorksheet.cell("@B32")
        cell.value = 123

        # stop mock server
        sendClose(socket)
        thread.join()
        context.destroy()

    def test_integration_test_default_reactor_fail(self):
        # start mock server
        context = zmq.Context.instance()
        port = findNewSocketPort()
        thread = startREPServerOnThread(False, port, context, self.onReceive)
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
        sendClose(socket)
        thread.join()
        context.destroy()


if __name__ == '__main__':
    unittest.main()
