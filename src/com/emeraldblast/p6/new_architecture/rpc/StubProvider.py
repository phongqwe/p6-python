from abc import ABC
from typing import Optional

from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.proto.service.CellService_pb2_grpc import CellServiceStub
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub


class StubProvider(ABC):
    def getChannel(self) -> Optional:
        raise NotImplementedError()

    @property
    def wbService(self)->Optional[WorkbookServiceStub]:
        raise NotImplementedError()
    @property
    def cellService(self) -> Optional[CellServiceStub]:
        raise NotImplementedError()

    def setRpcInfo(self, rpcInfo: Optional[RpcInfo]):
        raise NotImplementedError()

    @property
    def rpcInfo(self) -> Optional[RpcInfo]:
        raise NotImplementedError()
