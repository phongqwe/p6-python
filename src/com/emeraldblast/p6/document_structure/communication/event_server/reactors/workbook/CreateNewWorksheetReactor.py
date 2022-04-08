from typing import Callable

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data.request.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.response.CreateNewWorksheetData import \
    CreateNewWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetRequestProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class CreateNewWorksheetReactor(EventReactor[bytes, CreateNewWorksheetResponse]):
    # def __init__(self, uid:str,wbGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
    def __init__(self, uid:str,wbGetter: WbGetter):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> CreateNewWorksheetResponse:
        protoObj = CreateNewWorksheetRequestProto()
        protoObj.ParseFromString(data)
        request = CreateNewWorksheetRequest.fromProto(protoObj)
        wbKey = request.workbookKey
        newSheetName = request.newWorksheetName

        getWbRs = self._wbGetter(request.workbookKey)

        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            createRs = wb.createNewWorksheetRs(newSheetName)
            if createRs.isOk():
                return CreateNewWorksheetResponse(
                    workbookKey = wbKey,
                    newWorksheetName = createRs.value.name,
                    isError = False,
                )
            else:
                return CreateNewWorksheetResponse(
                    workbookKey = wbKey,
                    newWorksheetName = newSheetName,
                    isError = True,
                    errorReport = createRs.err
                )
        else:
            return CreateNewWorksheetResponse(
                workbookKey = wbKey,
                newWorksheetName = newSheetName,
                isError = True,
                errorReport = getWbRs.err
            )