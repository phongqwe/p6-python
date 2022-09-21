import unittest

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellUpdateEntry import CellUpdateEntry
from com.qxdzbc.p6.worksheet.rpc_data_structure.MultiCellUpdateRequest import MultiCellUpdateRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId


class MultiCellUpdateRequest_test(unittest.TestCase):
    def test_toProto(self):
        o = MultiCellUpdateRequest(
            wsId = WorksheetId(wbKey = WorkbookKeys.fromNameAndPath("wb1"),wsName = "s1"),
            updateEntries = [
                CellUpdateEntry(
                    cellAddress = CellAddresses.fromLabel("QT12"),
                    content = CellContent.fromAny(123)
                ),
                CellUpdateEntry(
                    cellAddress = CellAddresses.fromLabel("MM11"),
                    content = CellContent.fromAny(123)
                )
            ]
        )
        p = o.toProtoObj()
        self.assertEqual(o.wsId.toProtoObj(),p.wsId)
        self.assertEqual(list(map(lambda e:e.toProtoObj(),o.updateEntries)),list(p.updateEntries))

    # def test_fromProtoBytes(self):
    #     proto = CellMultiUpdateRequestProto()
    #     proto.workbookKey.CopyFrom(WorkbookKeys.fromNameAndPath("b123",None).toProtoObj())
    #     proto.worksheetName = "Sheet1"
    #
    #     contentProto = CellUpdateContentProto()
    #     contentProto.formula = "formula_123"
    #     contentProto.literal = "literal_abc"
    #     entryProto = CellUpdateEntryProto()
    #     entryProto.content.CopyFrom(contentProto)
    #     addr = CellAddresses.fromLabel("Q12")
    #     entryProto.cellAddress.CopyFrom(addr.toProtoObj())
    #
    #     proto.cellUpdate.extend([entryProto])
    #
    #     c = CellMultiUpdateRequest.fromProtoBytes(proto.SerializeToString())




if __name__ == '__main__':
    unittest.main()
