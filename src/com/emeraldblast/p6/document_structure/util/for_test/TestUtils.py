import socket
import threading
from pathlib import Path

import zmq

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.app.AppImp import AppImp
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet





def compareWs(ws1:Worksheet, ws2:Worksheet)->bool:
    return ws1.compareWith(ws2)


def sampleWb(name):
    wb = WorkbookImp(name)
    s1 = wb.createNewWorksheet("Sheet1")
    s2 = wb.createNewWorksheet("Sheet2")
    s1.cell((1, 1)).value = 11
    s1.cell((2, 2)).value = 22
    s1.cell((3, 3)).value = 33
    s2.cell((1, 1)).value = 211
    s2.cell((2, 2)).value = 222
    s2.cell((3, 3)).value = 233
    return wb

def sampleApp()->App:
    wb = sampleWb("Book1")
    wb2 = sampleWb("Book2")
    wb3 = sampleWb("Book3")
    app = AppImp()
    app.wbContainer.addWorkbook(wb)
    app.wbContainer.addWorkbook(wb2)
    app.wbContainer.addWorkbook(wb3)
    return app

def findNewSocketPort():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def startREPServer(isOk, port, zContext, onReceive):
    repSocket = zContext.socket(zmq.REP)
    repSocket.bind(f"tcp://*:{port}")

    while True:
        receive = repSocket.recv()
        if receive == b"close":
            break
        onReceive(receive)
        if isOk:
            repSocket.send("ok".encode())
        else:
            repSocket.send("fail".encode())
    repSocket.close()


def startREPServerOnThread(isOk, port, zContext, onReceive) -> threading.Thread:
    thread = threading.Thread(target = startREPServer, args = [isOk, port, zContext, onReceive])
    thread.daemon = True
    thread.start()
    return thread

def sendClose(_socket):
    _socket.send("close".encode())

class MockToProto(ToProto):
    def __init__(self,str):
        self.str = str
    def toProtoObj(self):
        raise NotImplementedError

    def toProtoBytes(self):
        return self.str

