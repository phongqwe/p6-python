from typing import Optional, Callable

import grpc

from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.emeraldblast.p6.proto.rpc.app.service.AppService_pb2_grpc import AppServiceStub
from com.emeraldblast.p6.proto.rpc.cell.service.CellService_pb2_grpc import CellServiceStub
from com.emeraldblast.p6.proto.rpc.workbook.service.WorkbookService_pb2_grpc import WorkbookServiceStub


class InsecureRpcStubProvider(RpcStubProvider):

    def __init__(
            self,
            cellServiceProvider: Callable[[grpc.Channel], CellServiceStub],
            wbServiceProvider: Callable[[grpc.Channel], WorkbookServiceStub],
            appServiceProvider: Callable[[grpc.Channel], AppServiceStub],
            rpcInfo: Optional[RpcInfo] = None,
    ):
        self.wbServiceProvider = wbServiceProvider
        self.cellServiceProvider = cellServiceProvider
        self._appServiceProvider = appServiceProvider
        self._rpcInfo = rpcInfo
        self._cellService = None
        self._channel = None
        self._wbService = None
        self._appService = None
        self.__createObj()

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
            self._channel = grpc.insecure_channel(f"{rpcInfo.host}:{rpcInfo.port}")
            self._cellService = self.cellServiceProvider(self._channel)
            self._wbService = self.wbServiceProvider(self._channel)
            self._appService = self._appServiceProvider(self._channel)

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
