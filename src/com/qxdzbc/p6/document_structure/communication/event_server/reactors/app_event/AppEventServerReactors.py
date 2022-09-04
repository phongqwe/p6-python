import uuid

from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.CloseWorkbookReactor import \
    CloseWorkbookReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.CreateNewWorkbookReactor import \
    CreateNewWorkbookReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.LoadWorkbookReactor import \
    LoadWorkbookReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.SaveWorkbookReactor import \
    SaveWorkbookReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.SetActiveWorksheetReactor import \
    SetActiveWorksheetReactor


class AppEventServerReactors:
    def __init__(self, workbookGetter: WbGetter, appGetter: AppGetter):
        self.wbGetter = workbookGetter
        self.appGetter = appGetter

    def loadWbReactor(self)->'LoadWorkbookReactor':
        return LoadWorkbookReactor(self.appGetter)

    def setActiveWorksheetReactor(self) -> SetActiveWorksheetReactor:
        return SetActiveWorksheetReactor(
            uid = str(uuid.uuid4()),
            appGetter = self.appGetter)

    def saveWorkbookReactor(self) -> SaveWorkbookReactor:
        return SaveWorkbookReactor(self.appGetter)
    
    def createNewWorkbookReactor(self)->CreateNewWorkbookReactor:
        return CreateNewWorkbookReactor(self.appGetter)

    def closeWorkbookReactor(self)->CloseWorkbookReactor:
        return CloseWorkbookReactor(self.appGetter)