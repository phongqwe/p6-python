import unittest
from dataclasses import dataclass

from typing import Optional

from com.qxdzbc.p6.app.App import App
from com.qxdzbc.p6.app.GlobalScope import setIPythonGlobals
from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.app.TopLevel import getApp
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import LoadDataRequestProto
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet import RpcWorksheet
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


@dataclass
class B:
    x: int
    v: Optional[str] = "Default v"


class Bench(unittest.TestCase):

    def test_q(self):
        import pandas as pd
        import numpy as np
        df = pd.DataFrame([[5, 2, np.nan], [9, 2, 4], [9, 2, 4]])
        print(df)
        print("====")
        for c in df:
            for num in df[c]:
                print(num)


    def test_configRpc(self):
        from com.qxdzbc.p6.rpc.RpcInfo import RpcInfo
        setIPythonGlobals(globals())
        app: RpcApp = getApp()
        rpcSP:RpcStubProvider = app.rpcSP
        port = 52533
        rpcInfo = RpcInfo(
            host="localhost",
            port=port
        )
        rpcSP.setRpcInfo(
            rpcInfo
        )

        # wb0:Workbook=app.getWorkbook(1)
        aw = app.activeWorkbook
        aws = app.activeWorksheet
        print(aw.key)
        # print(aws.wbKey)

        # app.printWorkbookSummary()
        # o = app.closeWorkbook(WorkbookKeys.fromNameAndPath("Book1"))
        # app.createNewWorkbook("WBBBB")
        # app.setActiveWorkbook(WorkbookKeys.fromNameAndPath("WBBBB"))
        # print(app.activeWorkbook)

        # app.loadWorkbookRs("/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w1.txt")
        # wbk = WorkbookKeys.fromNameAndPath("w1.txt","/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w1.txt")
        # app.saveWorkbookAtPath(wbk,"/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w2.txt")
