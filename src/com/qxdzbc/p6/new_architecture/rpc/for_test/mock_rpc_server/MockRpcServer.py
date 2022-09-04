from concurrent import futures
from typing import Callable

import grpc

from com.qxdzbc.p6.new_architecture.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.new_architecture.rpc.InsecureStubProvider import InsecureRpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.RpcInfo import RpcInfo


class MockRpcServer:
    port = 50052
    host = "localhost"
    rpInfo = RpcInfo(host = host, port = port)
    stubProvider = InsecureRpcStubProvider(
        rpcInfo = rpInfo,
        cellServiceProvider = RpcServiceContainer.cellService.provider,
        wbServiceProvider = RpcServiceContainer.wbService.provider,
        appServiceProvider = RpcServiceContainer.appService.provider,
        wsServiceProvider = RpcServiceContainer.wsService.provider
    )

    def __init__(self):
        self.server: grpc.Server = None
        self.adders = []

    def addServicer(self, adderServicerFunction: Callable[[grpc.Server], None]):
        self.adders.append(adderServicerFunction)

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
        for adder in self.adders:
            adder(server = self.server)
        self.server.add_insecure_port(f"[::]:{MockRpcServer.port}")
        self.server.start()

    def stop(self):
        if self.server:
            self.server.stop(grace = False)
