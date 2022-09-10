import sys

from dependency_injector import providers
from dependency_injector.wiring import inject

from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.di.DocumentContainer import DocumentContainer
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer


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
        rpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider
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