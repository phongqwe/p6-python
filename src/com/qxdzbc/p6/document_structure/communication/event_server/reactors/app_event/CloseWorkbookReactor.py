from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookRequest import \
    CloseWorkbookRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookResponse import \
    CloseWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import AppGetter
from com.qxdzbc.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor


class CloseWorkbookReactor(BaseEventReactor[bytes, CloseWorkbookResponse]):

    def __init__(self, appGetter: AppGetter):
        super().__init__()
        self.appGetter = appGetter

    def react(self, data: bytes) -> CloseWorkbookResponse:
        req = CloseWorkbookRequest.fromProtoBytes(data)
        app = self.appGetter().rootApp
        rs = app.closeWorkbookRs(req.workbookKey)
        
        response = CloseWorkbookResponse(
            isError = rs.isErr(),
            workbookKey = req.workbookKey,
            windowId = req.windowId,
            errorReport = None
        )
        if rs.isErr():
            response.errorReport = rs.err

        return response
