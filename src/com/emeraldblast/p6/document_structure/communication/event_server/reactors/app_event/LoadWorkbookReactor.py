from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookRequest import \
    LoadWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetResponse import \
    SetActiveWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import AppGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class LoadWorkbookReactor(BaseEventReactor[bytes, LoadWorkbookResponse]):
    def __init__(self, appGetter: AppGetter):
        super().__init__()
        self.appGetter = appGetter

    def react(self, data: bytes) -> LoadWorkbookResponse:
        req = LoadWorkbookRequest.fromProtoByte(data)
        app = self.appGetter()
        loadRs: Result[Workbook, ErrorReport] = app.loadWorkbookRsNoEvent(req.absolutePath)
        res = LoadWorkbookResponse(isError = loadRs.isErr())
        if loadRs.isOk():
            res.workbook = loadRs.value
        else:
            res.errorReport = loadRs.err
        return res
