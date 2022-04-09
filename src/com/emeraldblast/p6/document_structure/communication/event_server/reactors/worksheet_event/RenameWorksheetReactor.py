from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter

from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetResponse import \
    RenameWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class RenameWorksheetReactor(EventReactor[bytes, RenameWorksheetResponse]):

    def __init__(self, uid:str,wbGetter: WbGetter):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    @property
    def id(self) -> str:
        pass

    def react(self,data: bytes) -> RenameWorksheetResponseProto:
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
                    out = RenameWorksheetResponse(
                        workbookKey = wbKey,
                        oldName = oldName,
                        newName = newName,
                        index = wb.getIndexOfWorksheet(newName),
                        isError = False,
                    )
                    return out
                else:
                    out = RenameWorksheetResponse(
                        workbookKey = wbKey,
                        oldName = oldName,
                        newName = newName,
                        isError = True,
                        errorReport = renameRs.err
                    )
                    return out
            else:
                out = RenameWorksheetResponse(
                    workbookKey = wbKey,
                    oldName = oldName,
                    newName = newName,
                    isError = True,
                    errorReport = getWsRs.err
                )
                return out
        else:
            out = RenameWorksheetResponse(
                workbookKey = wbKey,
                newName = newName,
                oldName = oldName,
                isError = True,
                errorReport = getWbRs.err)
            return out
