from typing import Optional, Callable

import grpc

from com.qxdzbc.p6.rpc.RpcInfo import RpcInfo
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.proto.rpc.AppService_pb2_grpc import AppServiceStub
from com.qxdzbc.p6.proto.rpc.CellService_pb2_grpc import CellServiceStub
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class InsecureRpcStubProvider(RpcStubProvider):

    def __init__(
            self,
            cellServiceProvider: Callable[[grpc.Channel], CellServiceStub],
            wbServiceProvider: Callable[[grpc.Channel], WorkbookServiceStub],
            appServiceProvider: Callable[[grpc.Channel], AppServiceStub],
            wsServiceProvider:Callable[[grpc.Channel], WorksheetServiceStub],
            rpcInfo: Optional[RpcInfo] = None,
    ):
        self.wsServiceProvider = wsServiceProvider
        self.wbServiceProvider = wbServiceProvider
        self.cellServiceProvider = cellServiceProvider
        self._appServiceProvider = appServiceProvider
        self._rpcInfo = rpcInfo
        self._cellService = None
        self._channel = None
        self._wbService = None
        self._appService = None
        self._wsService = None
        self.__createObj()

    @property
    def wsService(self) -> Optional[WorksheetServiceStub]:
        if self._rpcInfo:
            return self._wsService
        else:
            return None

    @property
    def wbService(self) -> Optional[WorkbookServiceStub]:
        if self._rpcInfo:
            return self._wbService
        else:
            return None

    def setRpcInfo(self, rpcInfo: Optional[RpcInfo]):
        if rpcInfo is not None:
            self._rpcInfo = rpcInfo
            self.__createObj()
        else:
            self.__clearObjs()

    @property
    def rpcInfo(self) -> Optional[RpcInfo]:
        return self._rpcInfo

    def __createObj(self):
        rpcInfo = self._rpcInfo
        if rpcInfo is not None:
            self._channel = grpc.insecure_channel(
                f"{rpcInfo.host}:{rpcInfo.port}",
                # options = (('grpc.enable_http_proxy', 0),)
            )
            self._cellService = self.cellServiceProvider(self._channel)
            self._wbService = self.wbServiceProvider(self._channel)
            self._appService = self._appServiceProvider(self._channel)
            self._wsService = self.wsServiceProvider(self._channel)

    def __clearObjs(self):
        self._cellService = None
        self._channel = None
        self._appService = None
        self._wbService = None

    @property
    def appService(self) -> Optional[AppServiceStub]:
        if self._rpcInfo:
            return self._appService
        else:
            return None

    @property
    def cellService(self) -> Optional[CellServiceStub]:
        if self._rpcInfo:
            return self._cellService
        else:
            return None

    def getChannel(self) -> Optional:
        if self._rpcInfo:
            return self._channel
        else:
            return None
