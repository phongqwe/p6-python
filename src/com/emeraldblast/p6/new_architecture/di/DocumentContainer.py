from dependency_injector import containers, providers

from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class DocumentContainer(containers.DeclarativeContainer):
    rpcWb = providers.Factory(
        RpcWorkbook
    )