from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.script_event.new_script.NewScriptReactor import \
    NewScriptReactor


class ScriptEventReactors:
    def __init__(self, wbGetter: WbGetter, appGetter: AppGetter):
        self.wbGetter = wbGetter
        self.appGetter = appGetter

    def newScriptReactor(self)->NewScriptReactor:
        return NewScriptReactor(
            wbGetter = self.wbGetter,
            appGetter = self.appGetter
        )
