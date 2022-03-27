from typing import Optional, Union

import zmq

from bicp_document_structure.app.App import App
from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from bicp_document_structure.file.loader.P6FileLoader import P6FileLoader
from bicp_document_structure.file.loader.P6FileLoaders import P6FileLoaders
from bicp_document_structure.file.saver.P6FileSaver import P6FileSaver
from bicp_document_structure.file.saver.P6FileSavers import P6FileSavers
from bicp_document_structure.message.SocketProvider import SocketProvider
from bicp_document_structure.message.SocketProviderImp import SocketProviderImp
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.message.event.reactor.EventReactorContainers import EventReactorContainers
from bicp_document_structure.message.event.reactor.StdReactorProvider import StdReactorProvider
from bicp_document_structure.message.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.util.result.Results import Results
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.WorkbookWrapper import WorkbookWrapper
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class AppImp(App):
    """
    Standard implementation of App interface
    """

    def __init__(self,
                 workbookContainer: Optional[WorkbookContainer] = None,
                 loader: Optional[P6FileLoader] = None,
                 saver: Optional[P6FileSaver] = None,
                 socketProvider: SocketProvider | None = None,
                 cellEventReactorContainer: EventReactorContainer[CellEventData] | None = None,
                 ):
        if workbookContainer is None:
            workbookContainer = WorkbookContainerImp()

        self.__wbCont: WorkbookContainer = workbookContainer
        # x: set default active workbook to the first workbook if possible
        if self.__wbCont.isNotEmpty():
            self.__activeWorkbook: Optional[Workbook] = self.__wbCont.getWorkbookByIndex(0)
        else:
            self.__activeWorkbook: Optional[Workbook] = None

        if loader is None:
            loader = P6FileLoaders.standard()
        if saver is None:
            saver = P6FileSavers.standard()
        self.__wbLoader: P6FileLoader = loader
        self.__wbSaver: P6FileSaver = saver
        self.__newBookIndex: int = 0

        if socketProvider is None:
            socketProvider = SocketProviderImp()
        self.__socketProvider: SocketProvider = socketProvider
        if cellEventReactorContainer is None:
            cellEventReactorContainer = EventReactorContainers.mutable()
        self.__reactorContainer: EventReactorContainer[CellEventData] = cellEventReactorContainer
        self.__reactorProvider = StdReactorProvider(self._getSocketProvider)
        self.__zcontext = zmq.Context.instance()
        self.initBaseReactor()

    @property
    def zContext(self):
        return self.__zcontext

    def initBaseReactor(self):
        """create base reactors """
        container = self.__reactorContainer
        provider = self.__reactorProvider
        container.addReactor(P6Events.Cell.UpdateValueEvent, provider.cellUpdateValue())
        container.addReactor(P6Events.Workbook.Rename.event, provider.worksheetRename())
        container.addReactor(P6Events.Workbook.CreateNewWorksheet.event, provider.createNewWorksheet())

    @property
    def eventReactorContainer(self) -> EventReactorContainer:
        return self.__reactorContainer

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
    def _fileSaver(self) -> P6FileSaver:
        return self.__wbSaver

    @property
    def _fileLoader(self) -> P6FileLoader:
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

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        setRs = self.setActiveWorkbookRs(indexOrNameOrKey)
        return Results.extractOrRaise(setRs)

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        wb = self.getWorkbook(indexOrNameOrKey)
        if wb is not None:
            if isinstance(wb, WorkbookWrapper):
                self.__activeWorkbook = wb.innerWorkbook
            else:
                self.__activeWorkbook = wb
            return Ok(self.__activeWorkbook)
        else:
            return Err(
                ErrorReport(
                    header = AppErrors.WorkbookNotExist.header,
                    data = AppErrors.WorkbookNotExist.Data(indexOrNameOrKey)
                )
            )

    @property
    def wbContainer(self) -> WorkbookContainer:
        return self.__wbCont

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        if self.activeWorkbook is not None:
            return self.activeWorkbook.activeWorksheet
        else:
            return None

    def createDefaultNewWorkbookRs(self, name: str | None = None) -> Result[Workbook, ErrorReport]:
        newWbRs: Result[Workbook, ErrorReport] = self.createNewWorkbookRs(name)
        if newWbRs.isOk():
            wb = newWbRs.value
            wb.createNewWorksheetRs()
        return newWbRs

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        createRs: Result[Workbook, ErrorReport] = self.createNewWorkbookRs(name)
        return Results.extractOrRaise(createRs)

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
                ErrorReport(
                    header = AppErrors.WorkbookAlreadyExist.header,
                    data = AppErrors.WorkbookAlreadyExist.Data(name)
                )
            )
