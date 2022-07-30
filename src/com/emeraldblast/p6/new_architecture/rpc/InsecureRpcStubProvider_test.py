import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureRpcStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo


class InsecureRpcStubProvider_test(unittest.TestCase):
    def test_setRcpInfo(self):
        mockProvider = MagicMock(return_value = MagicMock())

        p = InsecureRpcStubProvider(
            cellServiceProvider = mockProvider,
            wbServiceProvider = mockProvider,
            appServiceProvider = mockProvider,
        )

        for e in [p.appService, p.wbService, p.cellService]:
            self.assertIsNone(e)

        p.setRpcInfo(
            RpcInfo(
                host="localhost",
                port=12345
            )
        )
        for e in [p.appService, p.wbService, p.cellService]:
            self.assertIsNotNone(e)



if __name__ == '__main__':
    unittest.main()
