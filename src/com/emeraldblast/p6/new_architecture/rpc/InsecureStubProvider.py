from typing import Optional, Callable

import grpc

from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import RpcServiceProvider
from com.emeraldblast.p6.proto.service.CellService_pb2_grpc import CellServiceStub
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub


class InsecureRpcServiceProvider(RpcServiceProvider):

    def __init__(
            self,
            cellServiceProvider: Callable[[grpc.Channel], CellServiceStub],
            wbServiceProvider:Callable[[grpc.Channel],WorkbookServiceStub],
            rpcInfo: Optional[RpcInfo] = None,
    ):
        self.wbServiceProvider = wbServiceProvider
        self.cellServiceProvider = cellServiceProvider
        self._rpcInfo = rpcInfo
        self._cellService = None
        self._channel = None
        self._wbService = None
        self.__createObj()

    @property
    def wbService(self) -> Optional[WorkbookServiceStub]:
        return self._wbService

    def setRpcInfo(self, rpcInfo: Optional[RpcInfo]):
        if rpcInfo is not None:
            self._rpcInfo = rpcInfo
        else:
            self.__clearObjs()

    @property
    def rpcInfo(self) -> Optional[RpcInfo]:
        return self._rpcInfo

    def __createObj(self):
        rpcInfo = self._rpcInfo
        if rpcInfo is not None:
            self._channel = grpc.insecure_channel(f"{rpcInfo.host}:{rpcInfo.port}")
            # self._cellService = CellServiceStub(self._channel)
            # self._wbService = WorkbookServiceStub(self._channel)
            self._cellService = self.cellServiceProvider(self._channel)
            self._wbService = self.wbServiceProvider(self._channel)

    def __clearObjs(self):
        self._cellService = None
        self._channel = None

    @property
    def cellService(self) -> Optional[CellServiceStub]:
        return self._cellService

    def getChannel(self) -> Optional:
        return self._channel
