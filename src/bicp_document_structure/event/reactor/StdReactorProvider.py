import uuid
from functools import partial
from typing import Callable

from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.event.reactor.EventReactorFactory import EventReactorFactory
from bicp_document_structure.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.event.reactor.ReactorProvider import ReactorProvider
from bicp_document_structure.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.SocketProvider import SocketProvider
from bicp_document_structure.message.sender.MessageSender import MessageSender


class StdReactorProvider(ReactorProvider):

    def __init__(self, socketProviderGetter: Callable[[], SocketProvider]):
        self.__spg = socketProviderGetter
        self.__cellUpdateValue: CellReactor | None = None
        self.__cellUpdateScript: CellReactor | None = None
        self.__cellFormulaUpdate: CellReactor | None = None
        self.__cellClearScriptResult: CellReactor | None = None

        self.__colReRun: ColumnReactor | None = None
        self.__rangeReRun: RangeReactor | None = None
        self.__worksheetReRun: WorksheetReactor | None = None
        self.__workbookReRun: WorkbookReactor | None = None

    def cb(self, msgType: MsgType, data: WithWorkbookData):
        """
        rerun the whole workbook, serialize the workbook to json, then send the json in a zmq message to a predesignated socket.
        If sockets are not available, don't do anything
        """
        socketProvider = self.__spg()
        wb = data.workbook
        wb.reRun()
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ(
                    socket = socket,
                    msg = P6Message(
                        header = P6MessageHeader(str(uuid.uuid4()), msgType),
                        content = wb))
                if replyRs.isErr():
                    raise replyRs.err.toException()

    def cellUpdateValue(self) -> CellReactor:
        if self.__cellUpdateValue is None:
            self.__cellUpdateValue = EventReactorFactory.makeCellReactor(partial(self.cb, MsgType.CellUpdateValue))
        return self.__cellUpdateValue

    def cellUpdateScript(self) -> CellReactor:
        if self.__cellUpdateScript is None:
            self.__cellUpdateScript = EventReactorFactory.makeCellReactor(partial(self.cb, MsgType.CellUpdateScript))
        return self.__cellUpdateScript

    def cellUpdateFormula(self) -> CellReactor:
        if self.__cellFormulaUpdate is None:
            self.__cellFormulaUpdate = EventReactorFactory.makeCellReactor(partial(self.cb, MsgType.CellUpdateFormula))
        return self.__cellFormulaUpdate

    def cellClearScriptResult(self) -> CellReactor:
        if self.__cellClearScriptResult is None:
            self.__cellClearScriptResult = EventReactorFactory.makeCellReactor(
                partial(self.cb, MsgType.CellClearScriptResult))
        return self.__cellClearScriptResult

    def colReRun(self) -> ColumnReactor:
        if self.__colReRun is None:
            self.__colReRun = EventReactorFactory.makeColReactor(partial(self.cb, MsgType.ColReRun))
        return self.__colReRun

    def rangeReRun(self) -> RangeReactor:
        if self.__rangeReRun is None:
            self.__rangeReRun = EventReactorFactory.makeRangeReactor(partial(self.cb, MsgType.RangeReRun))
        return self.__rangeReRun

    def worksheetReRun(self) -> WorksheetReactor:
        if self.__worksheetReRun is None:
            self.__worksheetReRun = EventReactorFactory.makeRangeReactor(
                partial(self.cb, MsgType.WorksheetReRun))
        return self.__worksheetReRun

    def workbookCB(self, msgType: MsgType, data: WorkbookEventData):
        socketProvider = self.__spg()
        wb = data.workbook
        if socketProvider is not None:
            socket = socketProvider.reqSocketForUIUpdating()
            if socket is not None:
                replyRs = MessageSender.sendREQ(
                    socket = socket,
                    msg = P6Message(
                        header = P6MessageHeader(str(uuid.uuid4()), msgType),
                        content = wb))
                if replyRs.isErr():
                    raise replyRs.err.toException()

    def workbookReRun(self) -> WorkbookReactor:
        if self.__workbookReRun is None:
            self.__workbookReRun = EventReactorFactory.makeColReactor(partial(self.workbookCB, MsgType.WorkbookReRun))
        return self.__workbookReRun
