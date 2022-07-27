from abc import ABC

from dependency_injector import containers, providers

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureRpcServiceProvider
from com.emeraldblast.p6.proto.service.CellService_pb2_grpc import CellServiceStub
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub


class RpcServiceContainer(containers.DeclarativeContainer):

    cellService = providers.Factory(
        CellServiceStub,
    )

    wbService = providers.Factory(
        WorkbookServiceStub,
    )

    insecureRpcServiceProvider = providers.Singleton(
        InsecureRpcServiceProvider,
        rpcInfo = None,
        wbServiceProvider = wbService.provider,
        cellServiceProvider = cellService.provider
    )