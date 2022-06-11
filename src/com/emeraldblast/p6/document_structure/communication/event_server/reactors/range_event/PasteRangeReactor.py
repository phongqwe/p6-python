from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeRequest import \
    PasteRangeRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.paste_range.PasteRangeResponse import \
    PasteRangeResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.EventReactorErrors import \
    EventReactorErrors
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WsGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class PasteRangeReactor(BaseEventReactor[bytes, PasteRangeResponse]):

    def __init__(self, wsGetter: WsGetter):
        super().__init__()
        self.wsGetter = wsGetter

    def react(self, data: bytes) -> PasteRangeResponse:
        try:
            request: PasteRangeRequest = PasteRangeRequest.fromProtoBytes(data)
            windowId = None
            if request.windowId:
                windowId = request.windowId
            wsRs: Result[Worksheet, ErrorReport] = self.wsGetter(request.wsWb.workbookKey, request.wsWb.worksheetName)
            if wsRs.isOk():
                ws: Worksheet = wsRs.value.rootWorksheet
                pasteRs = ws.pasteProtoFromClipboardRs(anchorCell = request.anchorCell)
                if pasteRs.isOk():
                    ws.workbook.reRun()
                    wb = ws.workbook.rootWorkbook
                    return PasteRangeResponse(
                        isError = False,
                        workbookKey = wb.workbookKey,
                        newWorkbook = wb,
                        windowId = windowId
                    )
                else:
                    return PasteRangeResponse(
                        isError = True,
                        errorReport = pasteRs.err,
                        windowId = windowId,
                    )
            else:
                return PasteRangeResponse(
                    isError = True,
                    errorReport = wsRs.err,
                    windowId = windowId
                )
        except Exception as e:
            return PasteRangeResponse(
                isError = True,
                errorReport = CommonErrors.ExceptionErrorReport(e),
            )
