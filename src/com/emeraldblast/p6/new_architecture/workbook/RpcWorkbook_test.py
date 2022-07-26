import unittest

from com.emeraldblast.p6.new_architecture.rpc.InsecureStubProvider import InsecureStubProvider
from com.emeraldblast.p6.new_architecture.rpc.RpcInfo import RpcInfo
from com.emeraldblast.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class RpcWorkbook_test(unittest.TestCase):
    def test_sheetCount(self):
        wb=RpcWorkbook(
            name = "qwe",
            path = None,
            stubProvider = InsecureStubProvider(
                rpcInfo = RpcInfo(
                    host="localhost",
                    port=35823,
                )
            )
        )
        print(wb.sheetCount)

if __name__ == '__main__':
    unittest.main()
