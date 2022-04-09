import uuid

from com.emeraldblast.p6.document_structure.communication.event.data_structure.request.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.response.RenameWorksheetData import \
    RenameWorksheetResponseData
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.app.SetActiveWorksheetReactor import \
    SetActiveWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.cell.CellUpdateReactor import \
    CellUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook.DeleteWorksheetReactor import \
    DeleteWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class EventServerReactors:

    def __init__(self, workbookGetter: WbGetter, appGetter: AppGetter):
        self._wbGetter = workbookGetter
        self.__worksheetRenameReactor: EventReactor[P6Message, RenameWorksheetResponseProto] | None = None
        self.__appGetter = appGetter

    def setActiveWorksheetReactor(self) -> SetActiveWorksheetReactor:
        return SetActiveWorksheetReactor(
            uid = str(uuid.uuid4()),
            appGetter = self.__appGetter
        )

    def deleteWorksheetReactor(self) -> DeleteWorksheetReactor:
        reactor = DeleteWorksheetReactor(str(uuid.uuid4()), self._wbGetter)
        return reactor

    def createNewWorksheetReactor(self) -> CreateNewWorksheetReactor:
        reactor = CreateNewWorksheetReactor(str(uuid.uuid4()), self._wbGetter)
        return reactor

    def cellUpdateValueReactor(self) -> CellUpdateReactor:
        reactor = CellUpdateReactor(str(uuid.uuid4()), self._wbGetter)
        return reactor

    def renameWorksheet(self) -> EventReactor[bytes, RenameWorksheetResponseData]:
        if self.__worksheetRenameReactor is None:
            def cb(data: bytes) -> RenameWorksheetResponseProto:
                request = RenameWorksheetRequest.fromProtoBytes(data)
                wbKey: WorkbookKey = request.workbookKey
                oldName = request.oldName
                newName = request.newName

                getWbRs: Result[Workbook, ErrorReport] = self._wbGetter(wbKey)

                if getWbRs.isOk():
                    wb: Workbook = getWbRs.value
                    getWsRs = wb.getWorksheetRs(oldName)
                    if getWsRs.isOk():
                        renameRs: Result[None, ErrorReport] = getWsRs.value.renameRs(newName)
                        if renameRs.isOk():
                            out = RenameWorksheetResponseData(
                                workbookKey = wbKey,
                                oldName = oldName,
                                newName = newName,
                                index = wb.getIndexOfWorksheet(newName),
                                isError = False,
                            )
                            return out
                        else:
                            out = RenameWorksheetResponseData(
                                workbookKey = wbKey,
                                oldName = oldName,
                                newName = newName,
                                isError = True,
                                errorReport = renameRs.err
                            )
                            return out
                    else:
                        out = RenameWorksheetResponseData(
                            workbookKey = wbKey,
                            oldName = oldName,
                            newName = newName,
                            isError = True,
                            errorReport = getWsRs.err
                        )
                        return out
                else:
                    out = RenameWorksheetResponseData(
                        workbookKey = wbKey,
                        newName = newName,
                        oldName = oldName,
                        isError = True,
                        errorReport = getWbRs.err)
                    return out

            self.__worksheetRenameReactor = EventReactorFactory.makeBasicReactor(cb)
        return self.__worksheetRenameReactor
