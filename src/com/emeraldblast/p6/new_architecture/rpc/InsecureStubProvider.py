from typing import Optional

import grpc

from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import StubProvider
from com.emeraldblast.p6.proto.service.CellService_pb2_grpc import CellServiceStub


class InsecureStubProvider(StubProvider):
    def __init__(self, rpcInfo: Optional[RpcInfo] = None):
        self._rpcInfo = rpcInfo
        self._cellService = None
        self._channel = None
        self.__createObj()

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
            self._cellService = CellServiceStub(self._channel)

    def __clearObjs(self):
        self._cellService = None
        self._channel = None

    @property
    def cellService(self) -> Optional[CellServiceStub]:
        return self._cellService

    def getChannel(self)->Optional:
        return self._channel
