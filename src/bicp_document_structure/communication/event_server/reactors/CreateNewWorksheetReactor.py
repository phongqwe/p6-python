from typing import Callable

from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.BaseReactor import BasicReactor
from bicp_document_structure.communication.event.reactor.EventReactor import EventReactor, I, O
from bicp_document_structure.communication.proto.WorkbookProtoMsg_pb2 import CreateNewWorksheetRequestProto
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey

ResponseClazz = P6Events.Workbook.CreateNewWorksheet.Response
RequestClazz = P6Events.Workbook.CreateNewWorksheet.Request

class CreateNewWorksheetReactor(EventReactor[bytes, ResponseClazz]):
    def __init__(self, uid:str,wbGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> ResponseClazz:
        protoObj = CreateNewWorksheetRequestProto()
        protoObj.ParseFromString(data)
        request = RequestClazz.fromProto(protoObj)
        wbKey = request.workbookKey
        newSheetName = request.newWorksheetName

        getWbRs = self._wbGetter(request.workbookKey)

        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            createRs = wb.createNewWorksheetRs(newSheetName)
            if createRs.isOk():
                return ResponseClazz(
                    workbookKey = wbKey,
                    newWorksheetName = createRs.value.name,
                    isError = False,
                )
            else:
                return ResponseClazz(
                    workbookKey = wbKey,
                    newWorksheetName = newSheetName,
                    isError = True,
                    errorReport = createRs.err
                )
        else:
            return ResponseClazz(
                workbookKey = wbKey,
                newWorksheetName = newSheetName,
                isError = True,
                errorReport = getWbRs.err
            )