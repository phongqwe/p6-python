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

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from pandas import DataFrame, read_clipboard
import pyperclip

from com.emeraldblast.p6.document_structure.cell.CellContentImp import CellContentImp
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp

from py4j.java_gateway import JavaGateway, CallbackServerParameters
from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter, MapConverter, ListConverter

from com.emeraldblast.p6.proto.DocProtos_pb2 import CellIdProto
from com.emeraldblast.p6.proto.service import CellService_pb2
from com.emeraldblast.p6.proto.service.CellService_pb2_grpc import CellServiceStub
from com.emeraldblast.p6.proto.service.GetCell_pb2 import GetCellRequest


@dataclass
class B:
    x: int
    v: Optional[str] = "Default v"


class MyJavaClass(object):

    def __init__(self, gateway):
        self.gateway = gateway

    def notify(self, obj):
        # print("Notified by Java")
        # print(obj)
        # self.gateway.jvm.System.out.println("Hello from python!")
        return "A Return Value"

    def toString(self):
        return "qwe"

    class Java:
        implements = ["com.emeraldblast.p6.ui.example.MyAny"]
        # implements = ["kotlin.Any"]


class Bench(unittest.TestCase):

    def test_rpc(self):
        channel = grpc.insecure_channel('localhost:43271')
        stub = CellServiceStub(channel)
        request = GetCellRequest(
            cellId = CellIdProto(
                wbKey = WorkbookKeys.fromNameAndPath("Book1").toProtoObj(),
                wsName="Sheet1",
                cellAddress = CellAddresses.fromColRow(2,2).toProtoObj()
            )
        )
        out = stub.getCellValue(request)
        print(out)

    def test_py4j(self):
        gateway = JavaGateway(
            callback_server_parameters = CallbackServerParameters())
        listener = MyJavaClass(gateway)
        # gateway.entry_point.registerListener(listener)
        listener.notify(gateway)
        app = gateway.entry_point
        a = gateway.jvm.com.emeraldblast.p6.ui.example.A(123, "abc")
        b = B(1, "abc")
        l = [1, 2]
        l = ListConverter().convert(l, gateway._gateway_client)

        app.setAnything(listener)
        print(app.getAnything())
