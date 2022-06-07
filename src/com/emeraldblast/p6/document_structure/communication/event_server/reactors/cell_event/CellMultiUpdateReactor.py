from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateRequest import \
    CellMultiUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellMultiUpdateResponse import \
    CellMultiUpdateResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class CellMultiUpdateReactor(BaseEventReactor[bytes, CellMultiUpdateResponse]):

    def __init__(self, wbGetter: WbGetter):
        super().__init__()
        self.wbGetter = wbGetter

    def react(self, data: bytes) -> CellMultiUpdateResponse:
        req = CellMultiUpdateRequest.fromProtoBytes(data)
        wbRs = self.wbGetter(req.workbookKey)
        rt = CellMultiUpdateResponse(
            isError = False,
            workbookKey = req.workbookKey
        )
        if wbRs.isOk():
            wb:Workbook = wbRs.value
            wsRs = wb.getWorksheetRs(req.worksheetName)
            if wsRs.isOk():
                ws:Worksheet = wsRs.value
                for update in req.cellUpdateList:
                    content = update.content
                    if len(content.formula)!=0:
                        ws.cell(update.cellAddress).formula = content.formula
                    else:
                        ws.cell(update.cellAddress).value = content.literal
                wb.reRun()
                rt.newWorkbook = wb
            else:
                rt.isError=True
                rt.errorReport = wsRs.err
                rt.errorReport.loc = "CellMultiUpdateReactor"
                return rt
        else:
            rt.isError=True
            rt.errorReport = wbRs.err
            rt.errorReport.loc = "CellMultiUpdateReactor"
            return rt

        return rt
