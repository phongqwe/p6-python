import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto, IndWorksheetProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import LoadDataRequestProto
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.rpc_data_structure.LoadDataRequest import LoadDataRequest


class LoadDataRequest_test(unittest.TestCase):
    def test_toProto(self):
        protoWs = IndWorksheetProto()
        mockWs = MagicMock()
        mockWs.toProtoObj = MagicMock(return_value = protoWs)
        ca = CellAddresses.fromColRow(2, 3)
        o = LoadDataRequest(
            loadType = LoadType.OVERWRITE,
            ws = mockWs
        )
        p = o.toProtoObj()
        self.assertEqual(LoadDataRequestProto.LoadTypeProto.OVERWRITE, p.loadType)
        self.assertEqual(protoWs, p.ws)


if __name__ == '__main__':
    unittest.main()
