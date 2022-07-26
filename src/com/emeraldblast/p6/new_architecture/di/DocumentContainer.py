from dependency_injector import containers, providers

from com.emeraldblast.p6.new_architecture.di.ProtoServiceContainer import ProtoServiceContainer
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class DocumentContainer(ProtoServiceContainer):
    rpcWb = providers.Factory(
        RpcWorkbook,
        path = None,
    )