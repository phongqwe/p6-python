from dependency_injector import containers, providers

from com.qxdzbc.p6.rpc.InsecureStubProvider import InsecureRpcStubProvider
from com.qxdzbc.p6.proto.rpc.AppService_pb2_grpc import AppServiceStub
from com.qxdzbc.p6.proto.rpc.CellService_pb2_grpc import CellServiceStub
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class RpcServiceContainer(containers.DeclarativeContainer):

    cellService = providers.Factory(
        CellServiceStub,
    )

    wbService = providers.Factory(
        WorkbookServiceStub,
    )

    appService = providers.Factory(
        AppServiceStub
    )
    wsService = providers.Factory(
        WorksheetServiceStub
    )

    insecureRpcServiceProvider = providers.Singleton(
        InsecureRpcStubProvider,
        rpcInfo = None,
        wbServiceProvider = wbService.provider,
        cellServiceProvider = cellService.provider,
        appServiceProvider = appService.provider,
        wsServiceProvider = wsService.provider,
    )