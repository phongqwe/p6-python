from abc import ABC

from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.event.reactor.RangeEventReactor import RangeEventReactor
from bicp_document_structure.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.event.reactor.WorksheetReactor import WorksheetReactor


class ReactorProvider(ABC):

    def cellUpdateValue(self) -> CellReactor:
        raise NotImplementedError()

    def cellUpdateScript(self) -> CellReactor:
        raise NotImplementedError()

    def cellUpdateFormula(self) -> CellReactor:
        raise NotImplementedError()

    def cellClearScriptResult(self) -> CellReactor:
        raise NotImplementedError()

    def colReRun(self) -> ColumnReactor:
        raise NotImplementedError()

    def rangeReRun(self) -> RangeEventReactor:
        raise NotImplementedError()

    def worksheetReRun(self) -> WorksheetReactor:
        raise NotImplementedError()

    def workbookReRun(self) -> WorkbookReactor:
        raise NotImplementedError()
