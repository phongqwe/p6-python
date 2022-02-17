from typing import Optional, Union, Callable

from bicp_document_structure.app.App import App
from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultImp import RunResultImp
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.file.loader.P6FileLoader import P6FileLoader
from bicp_document_structure.file.loader.P6FileLoaders import P6FileLoaders
from bicp_document_structure.file.saver.P6FileSaver import P6FileSaver
from bicp_document_structure.file.saver.P6FileSavers import P6FileSavers
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.util.result.Results import Results
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class AppImp(App):
    """
    Standard implementation of App interface
    """

    def __init__(self,
                 workbookContainer: Optional[WorkbookContainer] = None,
                 runResult: Optional[RunResult] = None,
                 loader: Optional[P6FileLoader] = None,
                 saver: Optional[P6FileSaver] = None,
                 onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] | None = None):
        if workbookContainer is None:
            workbookContainer = WorkbookContainerImp()

        self.__wbCont: WorkbookContainer = workbookContainer
        self.__onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] | None = onCellChange

        # x: set default active workbook to the first if possible
        if self.__wbCont.isNotEmpty():
            self.__activeWorkbook: Optional[Workbook] = self.__wbCont.getWorkbookByIndex(0)
        else:
            self.__activeWorkbook: Optional[Workbook] = None

        if runResult is None:
            runResult = RunResultImp()
        self.__result: RunResult = runResult
        if loader is None:
            loader = P6FileLoaders.standard()
        if saver is None:
            saver = P6FileSavers.standard()
        self.__wbLoader: P6FileLoader = loader
        self.__wbSaver: P6FileSaver = saver
        self.__newBookIndex: int = 0

    ### >> App << ###

    @property
    def _fileSaver(self) -> P6FileSaver:
        return self.__wbSaver

    @property
    def _fileLoader(self) -> P6FileLoader:
        return self.__wbLoader

    def hasNoWorkbook(self) -> bool:
        return self.wbContainer.isEmpty()

    def _getOnCellChange(self) -> Callable[[Workbook, Worksheet, Cell, P6Event], None] | None:
        return self.__onCellChange

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        if self.__activeWorkbook is None:
            if self.hasNoWorkbook():
                return None
            else:
                self.__activeWorkbook = self.wbContainer.getWorkbookByIndex(0)
                return self.__activeWorkbook
        else:
            return self.__activeWorkbook

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        setRs = self.setActiveWorkbookRs(indexOrNameOrKey)
        return Results.extractOrRaise(setRs)

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        wb = self.getWorkbook(indexOrNameOrKey)
        if wb is not None:
            self.__activeWorkbook = wb
            return Ok(wb)
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
    def result(self) -> RunResult:
        return self.__result

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        if self.__activeWorkbook is not None:
            return self.__activeWorkbook.activeWorksheet
        else:
            return None

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
            wb = WorkbookImp(name, onCellChange = self.__onCellChange)
            self.wbContainer.addWorkbook(wb)
            return Ok(wb)
        else:
            return Err(
                ErrorReport(
                    header = AppErrors.WorkbookAlreadyExist.header,
                    data = AppErrors.WorkbookAlreadyExist.Data(name)
                )
            )
