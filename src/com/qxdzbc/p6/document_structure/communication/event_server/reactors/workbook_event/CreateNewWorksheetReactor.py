from com.qxdzbc.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetResponse import \
    CreateNewWorksheetResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.workbook_event.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetRequestProto


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
                rt= CreateNewWorksheetResponse(
                    workbookKey = wbKey,
                    newWorksheetName = newSheetName,
                    isError = True,
                    errorReport = createRs.err
                )
                rt.errorReport.loc = "CreateNewWorksheetReactor"
                return rt
        else:
            rt= CreateNewWorksheetResponse(
                workbookKey = wbKey,
                newWorksheetName = newSheetName,
                isError = True,
                errorReport = getWbRs.err
            )
            rt.errorReport.loc = "CreateNewWorksheetReactor"
            return rt