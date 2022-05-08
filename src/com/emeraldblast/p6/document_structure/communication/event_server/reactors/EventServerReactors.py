import uuid

from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCell import \
    DeleteCellResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMulti import \
    DeleteMultiResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app_event.SetActiveWorksheetReactor import \
    SetActiveWorksheetReactor
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
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class EventServerReactors:

    def __init__(self, workbookGetter: WbGetter, appGetter: AppGetter):
        self.wbGetter = workbookGetter
        self.appGetter = appGetter

    def setActiveWorksheetReactor(self) -> SetActiveWorksheetReactor:
        return SetActiveWorksheetReactor(
            uid = str(uuid.uuid4()),
            appGetter = self.appGetter
        )

    def deleteWorksheetReactor(self) -> DeleteWorksheetReactor:
        reactor = DeleteWorksheetReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def createNewWorksheetReactor(self) -> CreateNewWorksheetReactor:
        reactor = CreateNewWorksheetReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def cellUpdateValueReactor(self) -> CellUpdateReactor:
        reactor = CellUpdateReactor(str(uuid.uuid4()), self.wbGetter)
        return reactor

    def renameWorksheet(self) -> EventReactor[bytes, RenameWorksheetResponse]:
        return RenameWorksheetReactor(
            uid=str(uuid.uuid4()),
            wbGetter = self.wbGetter
        )
    def deleteCellReactor(self)->EventReactor[bytes,DeleteCellResponse]:
        return DeleteCellReactor(
            uid = str(uuid.uuid4()),
            wbGetter = self.wbGetter
        )
    def deleteMultiReactor(self)->EventReactor[bytes,DeleteMultiResponse]:
        return DeleteMultiReactor(
            uid = str(uuid.uuid4()),
            wbGetter = self.wbGetter
        )