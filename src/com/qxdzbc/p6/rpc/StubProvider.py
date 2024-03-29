from abc import ABC
from typing import Optional

from com.qxdzbc.p6.rpc.RpcInfo import RpcInfo
from com.qxdzbc.p6.proto.rpc.AppService_pb2_grpc import AppServiceStub
from com.qxdzbc.p6.proto.rpc.CellService_pb2_grpc import CellServiceStub
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class RpcStubProvider(ABC):
    """
    A central point to access to grpc stubs
    """
    def getChannel(self) -> Optional:
        raise NotImplementedError()

    @property
    def wsService(self) -> Optional[WorksheetServiceStub]:
        raise NotImplementedError()

    @property
    def wbService(self)->Optional[WorkbookServiceStub]:
        raise NotImplementedError()
    @property
    def cellService(self) -> Optional[CellServiceStub]:
        raise NotImplementedError()

    @property
    def appService(self)->Optional[AppServiceStub]:
        raise NotImplementedError()

    def setRpcInfo(self, rpcInfo: Optional[RpcInfo]):
        raise NotImplementedError()

    @property
    def rpcInfo(self) -> Optional[RpcInfo]:
        raise NotImplementedError()
