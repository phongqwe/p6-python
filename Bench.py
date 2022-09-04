import os
import unittest
from dataclasses import dataclass
from datetime import datetime

import time
from typing import Optional
from unittest.mock import MagicMock

import grpc
import numpy as np
import pandas
import pandas as pd
from grpc_tools import protoc

from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from pandas import DataFrame, read_clipboard
import pyperclip

from com.qxdzbc.p6.document_structure.cell.CellContentImp import CellContentImp
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.range.RangeImp import RangeImp
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.document_structure.worksheet.WorksheetImp import WorksheetImp

from py4j.java_gateway import JavaGateway, CallbackServerParameters
from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter, MapConverter, ListConverter


from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellIdProto


@dataclass
class B:
    x: int
    v: Optional[str] = "Default v"

from com.qxdzbc.p6.document_structure.app.TopLevel import *
from com.qxdzbc.p6.document_structure.app.GlobalScope import *
class Bench(unittest.TestCase):

    def test_configRpc(self):
        import json
        from com.qxdzbc.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions
        from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
        from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
        import zmq
        from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses

        from com.qxdzbc.p6.new_architecture.rpc.RpcInfo import RpcInfo

        setIPythonGlobals(globals())
        app:App = getRpcApp()
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