import sys

from dependency_injector import containers, providers
from dependency_injector.wiring import inject

from com.emeraldblast.p6.new_architecture.app.RpcApp import RpcApp
from com.emeraldblast.p6.new_architecture.di.DocumentContainer import DocumentContainer
from com.emeraldblast.p6.new_architecture.di.RpcServiceContainer import RpcServiceContainer
from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureRpcServiceProvider
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class BF:
    def __init__(self,bn):
        self._bn = bn

    def b(self):
        return self._bn
class Summer:
    def __init__(self,a,bf):
        self._a = a
        self._bf=bf

    def sum(self,x1,x2):
        return x1+x2+self._a + self._bf.b()

class Container(DocumentContainer):
    rpcApp = providers.Singleton(
        RpcApp,
        rpcServiceProvider = RpcServiceContainer.insecureRpcServiceProvider
    )

    bf = providers.Singleton(
        BF,
        bn = 333
    )

    summer = providers.Singleton(
        Summer,
        a=123,
        bf = bf
    )
    summer2 = providers.Factory(
        Summer,
        bf=bf
    )

@inject
def main(summer:Summer =Container.summer()):
    app = Container.rpcApp()
    print(app)
    # s1 = Container.summer2(a=999,bf = BF(22229999))
    # s2 = Container.summer2(a=999)
    # print(s1.sum(123,321))

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules = [__name__])
    main(*sys.argv[1:])