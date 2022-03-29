from typing import Callable

from bicp_document_structure.message.event.data.RenameWorksheetOkData import RenameWorksheetData
from bicp_document_structure.message.event.reactor.EventReactor import EventReactor
from bicp_document_structure.message.proto.WorksheetProtoMsg_pb2 import RenameWorksheetProto, \
    RenameWorksheetRequestProto
from bicp_document_structure.util.ToProto import ToProto

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.event.reactor.BaseReactor import BasicReactor
from bicp_document_structure.message.event.reactor.CellReactor import CellReactor
from bicp_document_structure.message.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.message.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.message.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.message.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys


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
        self.__worksheetRenameReactor: WorkbookReactor[P6Message, RenameWorksheetProto] | None = None
        self.__worksheetRenameFail: WorksheetReactor | None = None

        self.__workbookReRun: WorkbookReactor | None = None

    # def createNewWorksheet(self) -> WorkbookReactor:
    #     def cb(wbEventData: WorkbookEventData):
    #         msg = StdReactorProvider.__createP6Msg(wbEventData.event, wbEventData.data)
    #         self._send(msg)
    #
    #     reactor = EventReactorFactory.makeWorkbookReactor(cb)
    #     return reactor

    # def cellUpdateValue(self) -> CellReactor:
    #     if self.__cellUpdateValue is None:
    #         event = P6Events.Cell.UpdateValueEvent
    #         self.__cellUpdateValue = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
    #     return self.__cellUpdateValue

    # def cellUpdateScript(self) -> CellReactor:
    #     if self.__cellUpdateScript is None:
    #         event = P6Events.Cell.UpdateScript
    #         self.__cellUpdateScript = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
    #     return self.__cellUpdateScript

    # def cellUpdateFormula(self) -> CellReactor:
    #     if self.__cellFormulaUpdate is None:
    #         event = P6Events.Cell.UpdateFormula
    #         self.__cellFormulaUpdate = EventReactorFactory.makeCellReactor(partial(self.stdCallback, event))
    #     return self.__cellFormulaUpdate

    # def cellClearScriptResult(self) -> CellReactor:
    #     if self.__cellClearScriptResult is None:
    #         event = P6Events.Cell.ClearScriptResult
    #         self.__cellClearScriptResult = EventReactorFactory.makeCellReactor(
    #             partial(self.stdCallback, event))
    #     return self.__cellClearScriptResult

    # def rangeReRun(self) -> RangeReactor:
    #     if self.__rangeReRun is None:
    #         event = P6Events.Range.ReRun
    #         self.__rangeReRun = EventReactorFactory.makeRangeReactor(partial(self.stdCallback, event))
    #     return self.__rangeReRun

    # def worksheetReRun(self) -> WorksheetReactor:
    #     if self.__worksheetReRun is None:
    #         event = P6Events.Worksheet.ReRun
    #         self.__worksheetReRun = EventReactorFactory.makeRangeReactor(
    #             partial(self.stdCallback, event))
    #     return self.__worksheetReRun
    #

    def renameWorksheet(self) -> BasicReactor[P6Message, RenameWorksheetData]:
        if self.__worksheetRenameReactor is None:
            def cb(p6Msg: P6Message) -> RenameWorksheetProto:
                receive = p6Msg.data

                protoRequest = RenameWorksheetRequestProto()
                protoRequest.ParseFromString(receive)
                wbKey: WorkbookKey = WorkbookKeys.fromProto(protoRequest.workbookKey)
                oldName = protoRequest.oldName
                newName = protoRequest.newName

                getWbRs: Result[Workbook, ErrorReport] = self._wbGetter(wbKey)

                if getWbRs.isOk():
                    wb: Workbook = getWbRs.value
                    renameRs: Result[None, ErrorReport] = wb.renameWorksheetRs(oldName, newName)
                    if renameRs.isOk():
                        out = RenameWorksheetData(
                            workbookKey = wbKey,
                            oldName = oldName,
                            newName = newName,
                            index = wb.getIndexOfWorksheet(newName),
                            isError = False,
                        )
                        return out
                    else:
                        out = RenameWorksheetData(
                            workbookKey = wbKey,
                            oldName = oldName,
                            newName = newName,
                            isError = True,
                            errorReport = renameRs.err
                        )
                        return out
                else:
                    out = RenameWorksheetData(
                        workbookKey = wbKey,
                        newName = newName,
                        oldName = oldName,
                        isError = True,
                        errorReport = getWbRs.err)
                    return out

            self.__worksheetRenameReactor = EventReactorFactory.makeBasicReactor(cb)
        return self.__worksheetRenameReactor
