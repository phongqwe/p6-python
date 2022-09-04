from dependency_injector import containers, providers

from com.qxdzbc.p6.new_architecture.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class DocumentContainer(RpcServiceContainer):
    rpcWb = providers.Factory(
        RpcWorkbook,
        path = None,
    )