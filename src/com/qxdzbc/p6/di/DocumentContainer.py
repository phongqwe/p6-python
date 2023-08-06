from dependency_injector import providers

from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook


class DocumentContainer(RpcServiceContainer):
    rpcWb = providers.Factory(
        RpcWorkbook,
        path = None,
    )