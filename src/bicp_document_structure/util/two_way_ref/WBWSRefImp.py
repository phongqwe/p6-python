from bicp_document_structure.util.two_way_ref.TwoWayRef import B, A
from bicp_document_structure.util.two_way_ref.WBWSRef import WBWSRef
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class WBWSRefImp(WBWSRef):

    def __init__(self,workbook,worksheet):
        self._wb = workbook
        self._ws = worksheet

    @property
    def workbook(self) -> Workbook:
        return self._wb

    @property
    def worksheet(self) -> Worksheet:
        return self._ws

    def cut(self):
        self._wb = None
        self._ws = None