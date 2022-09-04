from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookRequest import \
    CreateNewWorkbookRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookResponse import \
    CreateNewWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import AppGetter
from com.qxdzbc.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor


class CreateNewWorkbookReactor(BaseEventReactor[bytes, CreateNewWorkbookResponse]):

    def __init__(self, appGetter: AppGetter):
        super().__init__()
        self.appGetter = appGetter

    def react(self, data: bytes) -> CreateNewWorkbookResponse:
        req = CreateNewWorkbookRequest.fromProtoBytes(data)
        app = self.appGetter().rootApp
        rs = app.createDefaultNewWorkbookRs()
        rt = CreateNewWorkbookResponse(isError = rs.isErr(), windowId = req.windowId)
        if rs.isOk():
            rt.workbook = rs.value
        if rs.isErr():
            rt.errorReport = rs.err
        return rt
