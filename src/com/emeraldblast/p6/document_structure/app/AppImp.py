from typing import Optional, Union

import zmq

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.app.BaseApp import BaseApp
from com.emeraldblast.p6.document_structure.app.errors.AppErrors import AppErrors
from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.SocketProviderImp import SocketProviderImp
from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event_server.EventServer import EventServer
from com.emeraldblast.p6.document_structure.communication.event_server.EventServerImp import EventServerImp
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.EventServerReactors import \
    EventServerReactors
from com.emeraldblast.p6.document_structure.communication.notifier.InternalNotifierProvider import \
    InternalNotifierProvider
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainers import EventReactorContainers
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoaders import P6FileLoaders
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.emeraldblast.p6.document_structure.file.saver.P6FileSavers import P6FileSavers
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.util.Util import makeGetter
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class AppImp(BaseApp):
    """
    Standard implementation of App interface
    """

    def __init__(
            self,
            workbookContainer: Optional[WorkbookContainer] = None,
            loader: Optional[P6FileLoader] = None,
            saver: Optional[P6FileSaver] = None,
            socketProvider: SocketProvider | None = None,
            eventReactorContainer: EventReactorContainer[EventData] | None = None,
            scriptContainer: ScriptContainer | None = None,
    ):

        if scriptContainer is None:
            scriptContainer = ScriptContainerImp()
        self._scriptCont = scriptContainer

        if workbookContainer is None:
            workbookContainer = WorkbookContainerImp()

        self.__wbCont: WorkbookContainer = workbookContainer
        # x: set default active workbook to the first workbook if possible
        if self.__wbCont.isNotEmpty():
            self.__activeWorkbook: Optional[Workbook] = self.__wbCont.getWorkbookByIndex(0)
        else:
            self.__activeWorkbook: Optional[Workbook] = None

        if loader is None:
            loader = P6FileLoaders.proto()
        if saver is None:
            saver = P6FileSavers.proto()
        self.__wbLoader: P6FileLoader = loader
        self.__wbSaver: P6FileSaver = saver
        self.__newBookIndex: int = 0

        if socketProvider is None:
            socketProvider = SocketProviderImp()
        self.__socketProvider: SocketProvider = socketProvider
        if eventReactorContainer is None:
            eventReactorContainer = EventReactorContainers.mutable()
        self.__notifierContainer: EventReactorContainer[EventData] = eventReactorContainer
        self.__reactorProvider = InternalNotifierProvider(self._getSocketProvider)
        self.__zcontext = zmq.Context.instance()

        self.__initNotifiers()
        self._eventServer = EventServerImp(isDaemon = True)
        self._eventServerReactors = EventServerReactors(
            workbookGetter = self.getBareWorkbookRs,
            appGetter = makeGetter(self),
            rangeGetter = self.getRangeRs,
            wsGetter = self.getWorksheetRs
        )
        self.__setupEventServerReactors()
        self.__setupEventEmitter()

    @property
    def scriptContainer(self) -> ScriptContainer:
        return self._scriptCont

    @property
    def rootApp(self) -> 'App':
        return self

    @property
    def zContext(self):
        return self.__zcontext

    @property
    def eventServer(self) -> EventServer:
        return self._eventServer

    def __setupEventServerReactors(self):
        evSv = self._eventServer
        er = self._eventServerReactors
        table = P6EventTableImp.i()

        def addReactor(reactor):
            event = table.getEventFor(reactor)
            evSv.addReactor(event, reactor)

        reactorsForScript = [
            er.script.newScriptReactor()
        ]

        reactorForRange = [
            er.rangeToClipboardReactor(),
            er.rangeReactors.pasteRangeReactor()
        ]

        reactorForWb = [
            er.deleteWorksheetReactor(),
            er.createNewWorksheetReactor(),

        ]
        reactorForWs = [er.renameWorksheet(),
                        er.deleteCellReactor(),
                        er.deleteMultiReactor(), ]

        reactorForCell = [er.cellUpdateValueReactor(),
                          er.cellMultiUpdateReactor(), ]

        reactorForApp = [er.app.setActiveWorksheetReactor(),
                         er.app.saveWorkbookReactor(),
                         er.app.loadWbReactor(),
                         er.app.createNewWorkbookReactor(),
                         er.app.closeWorkbookReactor()]

        allReactors = [
            *reactorForRange,
            *reactorForWb,
            *reactorForWs,
            *reactorForCell,
            *reactorForApp,
            *reactorsForScript,
        ]
        for reactor in allReactors:
            addReactor(reactor)

    def __initNotifiers(self):
        """create internal reactors that will react to events from the app, workbooks, worksheets, cells, etc """
        container = self.__notifierContainer
        provider = self.__reactorProvider

        for event in P6Events.Script.allEvents():
            container.addReactor(event, provider.scriptNotifier())
        for event in P6Events.Cell.allEvents():
            container.addReactor(event, provider.cellNotifier())
        for event in P6Events.Workbook.allEvents():
            container.addReactor(event, provider.workbookNotifier())
        for event in P6Events.Worksheet.allEvents():
            container.addReactor(event, provider.worksheetNotifier())
        for event in P6Events.App.allEvents():
            container.addReactor(event, provider.appNotifier())
        for event in P6Events.Range.allEvents():
            container.addReactor(event, provider.appNotifier())

    def __setupEventEmitter(self):
        # self.__wbSaver=EventP6FileSaver.create(self.__wbSaver, self.__notifierContainer)
        # self.__wbLoader = EventP6FileLoader.create(self.__wbLoader, self.__notifierContainer)
        pass

    @property
    def eventNotifierContainer(self) -> EventReactorContainer:
        return self.__notifierContainer

    ### >> App << ###

    def _getSocketProvider(self) -> SocketProvider | None:
        return self.__socketProvider

    @property
    def socketProvider(self) -> SocketProvider | None:
        return self.__socketProvider

    @socketProvider.setter
    def socketProvider(self, socketProvider):
        self.__socketProvider = socketProvider

    @property
    def fileSaver(self) -> P6FileSaver:
        return self.__wbSaver

    @property
    def fileLoader(self) -> P6FileLoader:
        return self.__wbLoader

    def hasNoWorkbook(self) -> bool:
        return self.wbContainer.isEmpty()

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        if self.__activeWorkbook is None:
            if self.hasNoWorkbook():
                return None
            else:
                self.__activeWorkbook = self.wbContainer.getWorkbookByIndex(0)

        rt = self._makeEventWb(self.__activeWorkbook)
        return rt

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        wb = self.getWorkbookOrNone(indexOrNameOrKey)
        if wb is not None:
            self.__activeWorkbook = wb.rootWorkbook
            return Ok(self.__activeWorkbook)
        else:
            return Err(AppErrors.WorkbookNotExist.report(indexOrNameOrKey))

    @property
    def wbContainer(self) -> WorkbookContainer:
        return self.__wbCont

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        if self.activeWorkbook is not None:
            return self.activeWorkbook.activeWorksheet
        else:
            return None

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        if name is None:
            # x: create default name for new workbook
            name = "Workbook{}".format(self.__newBookIndex)
            while self.hasWorkbook(name):
                self.__newBookIndex += 1
                name = "Workbook{}".format(self.__newBookIndex)

        if not self.hasWorkbook(name):
            wb = WorkbookImp(name)
            eventNewWb = self._makeEventWb(wb)
            self.wbContainer.addWorkbook(wb)
            return Ok(eventNewWb)
        else:
            return Err(
                AppErrors.WorkbookAlreadyExist.report(name)
            )
