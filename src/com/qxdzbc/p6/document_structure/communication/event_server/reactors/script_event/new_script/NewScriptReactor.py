from com.qxdzbc.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.qxdzbc.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptRequest import \
    NewScriptRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptResponse import \
    NewScriptResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.qxdzbc.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor


class NewScriptReactor(BaseEventReactor[bytes, NewScriptResponse]):

    def __init__(self, wbGetter: WbGetter, appGetter: AppGetter):
        super().__init__()
        self.wbGetter = wbGetter
        self.appGetter = appGetter

    def react(self, data: bytes) -> NewScriptResponse:
        req: NewScriptRequest = NewScriptRequest.fromProtoBytes(data)
        wbKey = req.scriptEntry.key.workbookKey
        scriptContainer = None
        if wbKey is None:
            scriptContainer = self.appGetter().scriptContainer
        else:
            getWbRs = self.wbGetter(wbKey)
            if getWbRs.isOk():
                wb = getWbRs.value
                scriptContainer = wb.scriptContainer
            else:
                return NewScriptResponse(
                    errIndicator = ErrorIndicator.error(getWbRs.err)
                )
        addRs = scriptContainer.addScriptRs(req.scriptEntry.key.name, req.scriptEntry.script)
        if addRs.isOk():
            return NewScriptResponse(
                errIndicator = ErrorIndicator.noError()
            )
        else:
            return NewScriptResponse(
                errIndicator = ErrorIndicator.error(addRs.err)
            )
