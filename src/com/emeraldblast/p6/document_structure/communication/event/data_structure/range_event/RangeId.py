from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.DocProtos_pb2 import RangeIdProto


class RangeId(ToProto[RangeIdProto]):
    def toProtoObj(self) -> RangeIdProto:
        proto = RangeIdProto(
            workbookKey = self.workbookKey.toProtoObj(),
            worksheetName = self.worksheetName,
            rangeAddress = self.rangeAddress.toProtoObj(),
        )
        return proto
    
    @staticmethod
    def fromProto(proto:RangeIdProto)->'RangeId':
        return RangeId(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName,
            rangeAddress = RangeAddresses.fromProto(proto.rangeAddress),
        )

    def __init__(self, rangeAddress: RangeAddress, workbookKey: WorkbookKey, worksheetName: str):
        self.workbookKey = workbookKey
        self.worksheetName = worksheetName
        self.rangeAddress = rangeAddress


    def __eq__(self, other):
        if isinstance(other,RangeId):
            c1 = self.worksheetName == other.worksheetName
            c2 = self.workbookKey == other.workbookKey
            c3 = self.rangeAddress == other.rangeAddress
            return c1 and c2 and c3
        else:
            return False
