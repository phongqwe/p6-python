from abc import ABC

from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.RangeReactor import RangeReactor
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

    def rangeReRun(self) -> RangeReactor:
        raise NotImplementedError()

    def worksheetReRun(self) -> WorksheetReactor:
        raise NotImplementedError()

    def worksheetRenameOk(self) -> WorksheetReactor:
        raise NotImplementedError()

    def workbookReRun(self) -> WorkbookReactor:
        raise NotImplementedError()
