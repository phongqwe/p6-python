import uuid

from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCellResponse import \
    DeleteCellResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter, RangeGetter, WsGetter
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.app_event.AppEventServerReactors import \
    AppEventServerReactors
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.cell_event.CellMultiUpdateReactor import \
    CellMultiUpdateReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.cell_event.CellUpdateReactor import \
    CellUpdateReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.range_event.RangeEventReactors import \
    RangeEventReactors
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.range_event.RangeToClipboardReactor import \
    RangeToClipboardReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.script_event.ScriptEventReactors import \
    ScriptEventReactors
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.workbook_event.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.workbook_event.DeleteWorksheetReactor import \
    DeleteWorksheetReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteCellReactor import \
    DeleteCellReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.worksheet_event.DeleteMultiReactor import \
    DeleteMultiReactor
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.worksheet_event.RenameWorksheetReactor import \
    RenameWorksheetReactor
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactor import EventReactor


class EventServerReactors:

    def __init__(self,
                 workbookGetter: WbGetter,
                 appGetter: AppGetter,
                 rangeGetter:RangeGetter,
                 wsGetter:WsGetter):
        self.wbGetter = workbookGetter
        self.appGetter = appGetter
        self._app = AppEventServerReactors(self.wbGetter, self.appGetter)
        self.rangeGetter = rangeGetter
        self.wsGetter = wsGetter
        self.rangeReactors = RangeEventReactors(self.wsGetter)
        self.scriptReactors = ScriptEventReactors(
            wbGetter = workbookGetter,
            appGetter = appGetter
        )



    @property
    def script(self)->ScriptEventReactors:
        return self.scriptReactors
    @property
    def app(self)->AppEventServerReactors:
        return self._app

    def rangeToClipboardReactor(self)->RangeToClipboardReactor:
        return RangeToClipboardReactor(rangeGetter = self.rangeGetter)

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
    def deleteMultiReactor(self)->EventReactor[bytes, DeleteMultiResponse]:
        return DeleteMultiReactor(self.appGetter().getBareWorkbookRs)