import time
import unittest
from dataclasses import dataclass

from typing import Optional

from com.qxdzbc.p6.app.App import App
from com.qxdzbc.p6.app.GlobalScope import setIPythonGlobals
from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.app.TopLevel import getApp
from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import LoadDataRequestProto
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
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
        rpcSP: RpcStubProvider = app.rpcSP
        rpcInfo = RpcInfo(
            host = "localhost",
            port = 52533
        )
        rpcSP.setRpcInfo(
            rpcInfo
        )

        # wb0:Workbook=app.getWorkbook(1)
        awb = app.activeWorkbook
        # awb = app.getWorkbook("Book1")
        aws = app.activeWorksheet

        cell = aws.getCellAtAddress(CellAddresses.fromLabel("B3"))
        for x in range(10000):
            cell.value = x

        # for x in range(10000):
        #     aws.updateMultipleCellRs([
        #         CellUpdateEntry(
        #             CellAddresses.fromLabel("C1"),CellContent.fromAny(x)
        #         ),
        #         CellUpdateEntry(
        #             CellAddresses.fromLabel("A1"), CellContent.fromAny(x)
        #         )
        #     ])

        # rs = awb.removeAllWorksheetRs()
        # self.assertTrue(rs.isOk())

        # for x in range (1100):
        #     print(f"wb:{x}")
        #     app.createNewWorkbook()

        # for x in range(1000):
        #     print(f"ws: {x} ")
        #     z=awb.createNewWorksheet()
        #     time.sleep(1)

        # ar1=[
        #     [1,2,3],
        #     [4,5,6]
        # ]
        # import pandas as pd
        # df = pd.DataFrame({
        #     "a":ar1[0],
        #     "b":ar1[1]
        # })
        # aws.loadDataFrame(df,loadType = LoadType.OVERWRITE,keepHeader = False)

        # aws.load2DArray(
        #     [
        #         [100, 200, 300],
        #         [400, 500, 600]
        #     ],
        #     anchorCell = CellAddresses.fromLabel("B1"),
        #     loadType = LoadType.OVERWRITE
        # )

        # app.printWorkbookSummary()
        # o = app.closeWorkbook(WorkbookKeys.fromNameAndPath("Book1"))
        # app.createNewWorkbook("WBBBB")
        # app.setActiveWorkbook(WorkbookKeys.fromNameAndPath("WBBBB"))
        # print(app.activeWorkbook)

        # app.loadWorkbookRs("/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w1.txt")
        # wbk = WorkbookKeys.fromNameAndPath("w1.txt","/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w1.txt")
        # app.saveWorkbookAtPath(wbk,"/home/abc/Documents/gits/project2/p6/p6-app/src/test/resources/sampleWb/w2.txt")
