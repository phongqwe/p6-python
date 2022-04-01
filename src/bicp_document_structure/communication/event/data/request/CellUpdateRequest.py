from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.util.ToProto import ToProto, P

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.communication.proto.CellProtos_pb2 import CellUpdateRequestProto
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class CellUpdateRequest(ToProto[CellUpdateRequestProto]):
    def __init__(self, workbookKey:WorkbookKey, worksheetName:str, cellAddress:CellAddress, value:str, formula:str):
        self.formula = formula
        self.value = value
        self.cellAddress = cellAddress
        self.worksheetName = worksheetName
        self.workbookKey = workbookKey


    @staticmethod
    def fromProto(proto:CellUpdateRequestProto)->'CellUpdateRequest':
        rt = CellUpdateRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName,
            cellAddress = CellAddresses.fromProto(proto.cellAddress),
            value = proto.value,
            formula = proto.formula,
        )
        return rt

    @staticmethod
    def fromProtoBytes(protoByes:bytes)->'CellUpdateRequest':
        proto = CellUpdateRequestProto()
        proto.ParseFromString(protoByes)
        return CellUpdateRequest.fromProto(proto)

    def toProtoObj(self) -> CellUpdateRequestProto:
        rt = CellUpdateRequestProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.worksheetName = self.worksheetName
        rt.cellAddress.CopyFrom(self.cellAddress.toProtoObj())
        rt.value = self.value
        rt.formula = self.formula
        return rt
