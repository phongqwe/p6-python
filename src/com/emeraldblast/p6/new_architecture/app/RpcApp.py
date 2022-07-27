from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import RpcServiceProvider


class RpcApp(App):
    def __init__(
        self,
        rpcServiceProvider: RpcServiceProvider
    ):
        self.rpcServiceProvider = rpcServiceProvider

