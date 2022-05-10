from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse

from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateRequest import \
    CellMultiUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class CellMultiUpdateReactor(BaseEventReactor[bytes, WorkbookUpdateCommonResponse]):

    def __init__(self, wbGetter: WbGetter):
        super().__init__()
        self.wbGetter = wbGetter

    def react(self, data: bytes) -> WorkbookUpdateCommonResponse:
        req = CellMultiUpdateRequest.fromProtoBytes(data)
        wbRs = self.wbGetter(req.workbookKey)
        rt = WorkbookUpdateCommonResponse(
            isError = False,
            workbookKey = req.workbookKey
        )
        if wbRs.isOk():
            wb:Workbook = wbRs.value
            wsRs = wb.getWorksheetRs(req.worksheetName)
            if wsRs.isOk():
                ws:Worksheet = wsRs.value
                atLeast1FormulaWasUpdated = False
                for update in req.cellUpdateList:
                    content = update.content
                    if len(content.formula)!=0:
                        ws.cell(update.cellAddress).formula = content.formula
                        atLeast1FormulaWasUpdated = True
                    else:
                        ws.cell(update.cellAddress).value = content.literal
                if atLeast1FormulaWasUpdated:
                    wb.reRun()
                rt.newWorkbook = wb
            else:
                rt.isError=True
                rt.errorReport = wsRs.err
        else:
            rt.isError=True
            rt.errorReport = wbRs.err

        return rt