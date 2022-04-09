from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetRequest import \
    SetActiveWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter, \
    AppGetter

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetResponse import \
    SetActiveWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class SetActiveWorksheetReactor(EventReactor[bytes,SetActiveWorksheetResponse]):
    def __init__(self,uid:str, appGetter:AppGetter):
        self.appGetter = appGetter
        self._id = uid

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> SetActiveWorksheetResponse:
        request = SetActiveWorksheetRequest.fromProtoBytes(data)
        app = self.appGetter()
        setWbRs = app.setActiveWorkbookRs(request.workbookKey)

        response = SetActiveWorksheetResponse(
            workbookKey = request.workbookKey,
            worksheetName = request.worksheetName,
        )
        if setWbRs.isOk():
            wb:Workbook = setWbRs.value
            setSheetRs = wb.setActiveWorksheetRs(request.worksheetName)
            if setSheetRs.isOk():
                response.isError=False
                response.errorReport = None
                return response
            else:
                response.isError = True
                response.errorReport = setSheetRs.err
                return response
        else:
            response.isError = True
            response.errorReport = setWbRs.err
            return response