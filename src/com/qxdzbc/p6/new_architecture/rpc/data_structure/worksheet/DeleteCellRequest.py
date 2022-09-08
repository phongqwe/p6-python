from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import DeleteCellRequestProto


class DeleteCellRequest(ToProto[DeleteCellRequestProto]):
    def __init__(self, workbookKey:WorkbookKey,worksheetName:str,cellAddress:CellAddress):
        self.worksheetName = worksheetName
        self.cellAddress = cellAddress
        self.workbookKey = workbookKey

    def toProtoObj(self) -> DeleteCellRequestProto:
        rt = DeleteCellRequestProto()
        rt.worksheetName = self.worksheetName
        rt.cellAddress.CopyFrom(self.cellAddress.toProtoObj())
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return rt

    @staticmethod
    def fromProtoBytes(data:bytes)->'DeleteCellRequest':
        proto = DeleteCellRequestProto()
        proto.ParseFromString(data)
        return DeleteCellRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName,
            cellAddress = CellAddresses.fromProto(proto.cellAddress)
        )
