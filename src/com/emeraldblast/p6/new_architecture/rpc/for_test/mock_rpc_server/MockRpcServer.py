from concurrent import futures
from typing import Callable

import grpc

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo


class MockRpcServer:
    port = 50052
    host = "localhost"
    rpInfo = RpcInfo(host = host, port = port)
    stubProvider = InsecureStubProvider(
        rpcInfo = rpInfo
    )

    def __init__(self):
        self.server: grpc.Server = None
        self.adder = []

    def addServicer(self, adderServicerFunction: Callable[[grpc.Server], None]):
        self.adder.append(adderServicerFunction)

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
        for adder in self.adder:
            adder(server = self.server)
        self.server.add_insecure_port(f"[::]:{MockRpcServer.port}")
        self.server.start()

    def stop(self):
        if self.server:
            self.server.stop(grace = False)
