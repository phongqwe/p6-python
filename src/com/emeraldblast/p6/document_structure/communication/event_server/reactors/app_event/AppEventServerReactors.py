from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.LoadWorkbookReactor import \
    LoadWorkbookReactor


class AppEventServerReactors:
    def __init__(self, workbookGetter: WbGetter, appGetter: AppGetter):
        self.wbGetter = workbookGetter
        self.appGetter = appGetter

    def loadWbReactor(self)->'LoadWorkbookReactor':
        return LoadWorkbookReactor(self.appGetter)