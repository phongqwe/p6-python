from typing import Callable

from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetWrapper import WorksheetWrapper


class OverrideRenameWorksheet(WorksheetWrapper):
    """A decorator that override the renameRs function"""
    def __init__(self, innerWorksheet: Worksheet,
                 renameFunction: Callable[[str, str], Result[None, ErrorReport]] | None = None):
        super().__init__(innerWorksheet)
        self.renameFunction = renameFunction

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        if self.renameFunction is not None:
            """the rename result is entirely dictated by the external rename function"""
            return self.renameFunction(self.name, newName)
        else:
            self.internalRename(newName)
            return Ok(None)





