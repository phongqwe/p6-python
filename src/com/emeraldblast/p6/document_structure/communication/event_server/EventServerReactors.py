import uuid
from typing import Callable

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data.response.RenameWorksheetData import RenameWorksheetResponseData
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.CellUpdateReactor import CellUpdateReactor
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.CreateNewWorksheetReactor import \
    CreateNewWorksheetReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.CellReactor import CellReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactorFactory import EventReactorFactory
from com.emeraldblast.p6.document_structure.communication.internal_reactor.RangeReactor import RangeReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.WorkbookReactor import WorkbookReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.WorksheetReactor import WorksheetReactor
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto, \
    RenameWorksheetRequestProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class EventServerReactors:

    def __init__(self, workbookGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
        # self.__socketProvider = socketProviderGetter
        self._wbGetter = workbookGetter
        self.__cellUpdateValue: CellReactor | None = None
        self.__cellUpdateScript: CellReactor | None = None
        self.__cellFormulaUpdate: CellReactor | None = None
        self.__cellClearScriptResult: CellReactor | None = None

        self.__rangeReRun: RangeReactor | None = None

        self.__worksheetReRun: WorksheetReactor | None = None
        self.__worksheetRenameReactor: WorkbookReactor[P6Message, RenameWorksheetResponseProto] | None = None
        self.__worksheetRenameFail: WorksheetReactor | None = None

        self.__workbookReRun: WorkbookReactor | None = None

    def createNewWorksheetReactor(self) -> EventReactor[bytes, P6Events.Workbook.CreateNewWorksheet.Response]:
        reactor = CreateNewWorksheetReactor(str(uuid.uuid4()), self._wbGetter)
        return reactor

    def cellUpdateValueReactor(self) -> CellUpdateReactor:
        reactor = CellUpdateReactor(str(uuid.uuid4()), self._wbGetter)
        return reactor

    def renameWorksheet(self) -> EventReactor[bytes, RenameWorksheetResponseData]:
        if self.__worksheetRenameReactor is None:
            def cb(data: bytes) -> RenameWorksheetResponseProto:
                protoRequest = RenameWorksheetRequestProto()
                protoRequest.ParseFromString(data)
                request = P6Events.Worksheet.Rename.Request.fromProto(protoRequest)
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
