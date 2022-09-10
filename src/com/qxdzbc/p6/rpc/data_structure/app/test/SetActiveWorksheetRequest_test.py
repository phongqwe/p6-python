import unittest
from pathlib import Path

from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.app.SetActiveWorksheetRequest import SetActiveWorksheetRequest
from com.qxdzbc.p6.proto.AppProtos_pb2 import SetActiveWorksheetRequestProto


class SetActiveWorksheetRequest_test(unittest.TestCase):
    def test_fromProtoBytes(self):
        wk = WorkbookKeys.fromNameAndPath("B",Path("abc").absolute())

        proto = SetActiveWorksheetRequestProto()
        proto.workbookKey.CopyFrom(wk.toProtoObj())
        proto.worksheetName = "worksheetName"

        o = SetActiveWorksheetRequest.fromProtoBytes(proto.SerializeToString())
        self.assertEqual(wk,o.workbookKey)
        self.assertEqual(proto.worksheetName,o.worksheetName)
    def test_toProto(self):
        wk = WorkbookKeys.fromNameAndPath("B", Path("abc").absolute())
        request = SetActiveWorksheetRequest(
            workbookKey = wk,
            worksheetName = "Name123"
        )

        proto = request.toProtoObj()
        self.assertEqual(wk.toProtoObj(), proto.workbookKey)
        self.assertEqual(request.worksheetName, proto.worksheetName)



if __name__ == '__main__':
    unittest.main()
