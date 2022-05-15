from pathlib import Path

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookRequest import \
    SaveWorkbookRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import AppGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class SaveWorkbookReactor(BaseEventReactor[bytes, SaveWorkbookResponse]):

    def __init__(self, appGetter: AppGetter):
        super().__init__()
        self.appGetter = appGetter

    def react(self, data: bytes) -> SaveWorkbookResponse:
        request = SaveWorkbookRequest.fromProtoBytes(data)
        app = self.appGetter()
        wbKey = request.workbookKey
        targetPath = Path(request.path)
        pathIsDiff: bool = wbKey.filePath != targetPath
        saveRs: Result[Workbook | None, ErrorReport] = None
        newWbKey = wbKey

        if pathIsDiff:
            saveRs = app.saveWorkbookAtPathRs(wbKey, targetPath)
            newWbKey = newWbKey.setPath(targetPath)
        else:
            saveRs = app.saveWorkbookRs(wbKey)

        rt = SaveWorkbookResponse(
            isError = saveRs.isErr(),
            errorReport = saveRs.err,
            workbookKey = wbKey, # remember to return the old workbookKey
            path = request.path
        )
        return rt
