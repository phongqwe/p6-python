import unittest
from dataclasses import dataclass

from typing import Optional

from com.qxdzbc.p6.app.App import App
from com.qxdzbc.p6.app.GlobalScope import setIPythonGlobals
from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.app.TopLevel import getApp
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.worksheet import RpcWorksheet


@dataclass
class B:
    x: int
    v: Optional[str] = "Default v"


class Bench(unittest.TestCase):

    def test_configRpc(self):
        from com.qxdzbc.p6.rpc.RpcInfo import RpcInfo

        setIPythonGlobals(globals())
        app: RpcApp = getApp()
        rpcSP:RpcStubProvider = app.rpcSP
        port = 52500
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