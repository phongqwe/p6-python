from dependency_injector import containers, providers

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider


class ProtoServiceContainer(containers.DeclarativeContainer):
    insecureStubProvider = providers.Singleton(
        InsecureStubProvider,
        rpcInfo = None
    )
