from bicp_document_structure.util.two_way_ref.WBWSRef import WBWSRef
from bicp_document_structure.util.two_way_ref.WBWSRefImp import WBWSRefImp
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class Refs:
    @staticmethod
    def wbws(workbook:Workbook, worksheet:Worksheet)->WBWSRef:
        return WBWSRefImp(workbook, worksheet)