import socket
from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet

TestErrorReport = ErrorReport(
    header = ErrorHeader(
        errorCode = "123",
        errorDescription = "error for test"
    )
)

def compareWs(ws1:Worksheet, ws2:Worksheet)->bool:
    return ws1.compareContent(ws2)


def findNewSocketPort():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port
