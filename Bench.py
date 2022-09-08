import unittest
from dataclasses import dataclass

from typing import Optional

from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet


@dataclass
class B:
    x: int
    v: Optional[str] = "Default v"

from com.qxdzbc.p6.document_structure.app.TopLevel import *
from com.qxdzbc.p6.document_structure.app.GlobalScope import *
class Bench(unittest.TestCase):

    def test_configRpc(self):
        from com.qxdzbc.p6.new_architecture.rpc.RpcInfo import RpcInfo

        setIPythonGlobals(globals())
        app:App = getApp()
        rpcSP:RpcStubProvider = app.rpcSP
        port = 50052
        rpcInfo = RpcInfo(
            host="localhost",
            port=port
        )
        rpcSP.setRpcInfo(
            rpcInfo
        )
        wb0:RpcWorkbook=app.getWorkbook(0)
        ws1:RpcWorksheet = wb0.getWorksheet(0)

        # cell = ws1.cell("A1")
        # cell.copyFrom(ws1.cell("B2").id)
        print(ws1.cell("B2").value)