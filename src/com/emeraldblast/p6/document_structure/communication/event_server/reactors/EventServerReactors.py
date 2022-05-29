import uuid

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCell import \
    DeleteCellResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.AppEventServerReactors import \
    AppEventServerReactors
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell_event.CellMultiUpdateReactor import \
    CellMultiUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell_event.CellUpdateReactor import \
    CellUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook_event.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook_event.DeleteWorksheetReactor import \
    DeleteWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteCellReactor import \
    DeleteCellReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteMultiReactor import \
    DeleteMultiReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.worksheet_event.RenameWorksheetReactor import \
    RenameWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor




class EventServerReactors:

    def __init__(self, workbookGetter: WbGetter, appGetter: AppGetter):
        self.wbGetter = workbookGetter
        self.appGetter = appGetter
        self._app = AppEventServerReactors(self.wbGetter, self.appGetter)
    @property
    def app(self)->AppEventServerReactors:
        return self._app

    def deleteWorksheetReactor(self) -> DeleteWorksheetReactor:
        reactor = DeleteWorksheetReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def createNewWorksheetReactor(self) -> CreateNewWorksheetReactor:
        reactor = CreateNewWorksheetReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def cellUpdateValueReactor(self) -> CellUpdateReactor:
        reactor = CellUpdateReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def cellMultiUpdateReactor(self)->'CellMultiUpdateReactor':
        return CellMultiUpdateReactor(self.appGetter().getBareWorkbookRs)

    def renameWorksheet(self) -> EventReactor[bytes, RenameWorksheetResponse]:
        return RenameWorksheetReactor(
            uid=str(uuid.uuid4()),
            wbGetter = self.wbGetter
        )
    def deleteCellReactor(self)->EventReactor[bytes,DeleteCellResponse]:
        return DeleteCellReactor(
            uid = str(uuid.uuid4()),
            wbGetter = self.appGetter().getBareWorkbookRs
        )
    def deleteMultiReactor(self)->EventReactor[bytes, WorkbookUpdateCommonResponse]:
        return DeleteMultiReactor(self.appGetter().getBareWorkbookRs)