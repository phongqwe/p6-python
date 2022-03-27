from abc import ABC

from bicp_document_structure.util.two_way_ref.TwoWayRef import TwoWayRef, B, A
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class WBWSRef(ABC):
    @property
    def workbook(self)->Workbook:
        raise NotImplementedError()

    @property
    def worksheet(self)->Worksheet:
        raise NotImplementedError()

    def cut(self):
        raise NotImplementedError()

    def isValid(self)->bool:
        return self.workbook is not None and self.worksheet is not None

