from pathlib import Path
from typing import Optional, Union

from bicp_document_structure.app.App import App
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultImp import RunResultImp
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp
from bicp_document_structure.workbook.loader.WorkbookLoader import WorkbookLoader
from bicp_document_structure.workbook.saver.WorkbookSaver import WorkbookSaver
from bicp_document_structure.worksheet.Worksheet import Worksheet


class AppImp(App):
    """
    Standard implementation of App interface
    TODO implement this
    """

    def __init__(self,
                 workbookContainer: Optional[WorkbookContainer] = None,
                 runResult:Optional[RunResult]=None,
                 loader: Optional[WorkbookLoader] = None,
                 saver: Optional[WorkbookSaver] = None):
        if workbookContainer is None:
            workbookContainer = WorkbookContainerImp()

        self.__wbCont: WorkbookContainer = workbookContainer
        ## TODO set default active workbook to the first if possible
        if self.__wbCont.isNotEmpty():
            self.__activeWorkbook: Optional[Workbook] = self.__wbCont.getWorkbookByIndex(0)
        else:
            self.__activeWorkbook: Optional[Workbook] = None
        if runResult is None:
            runResult = RunResultImp()
        self.__result: RunResult = runResult
        self.__wbLoader: WorkbookLoader = loader
        self.__wbSaver: WorkbookSaver = saver

    ### >> App << ###

    def hasNoWorkbook(self) -> bool:
        return self.wbContainer.isEmpty()

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

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        return self.wbContainer.getWorkbookByIndex(index)

    def getWorkbookByKey(self, key: WorkbookKey) -> Optional[Workbook]:
        return self.wbContainer.getWorkbookByKey(key)

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        return self.wbContainer.getWorkbook(key)

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        wb = self.getWorkbook(indexOrNameOrKey)
        if wb is not None:
            self.__activeWorkbook = wb
            return
        else:
            raise ValueError("workbook at \"{n}\" does not exist, so it cannot be set as the active workbook.".format(
                n=str(indexOrNameOrKey)))

    @property
    def wbContainer(self) -> WorkbookContainer:
        return self.__wbCont

    @property
    def result(self) -> RunResult:
        return self.__result

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        if self.__activeWorkbook is not None:
            return self.__activeWorkbook.activeSheet
        else:
            return None

    def getWorkbookByName(self, name: str) -> Optional[Workbook]:
        return self.wbContainer.getWorkbookByName(name)

    def createNewWorkBook(self, name: str):
        wb = WorkbookImp(name)
        wb.workbookKey = WorkbookKeyImp(name, None)
        self.wbContainer.addWorkbook(wb)

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str, Path]):
        wb = self.__getWBOrRaiseError(nameOrIndexOrKey)
        saveRs = self.__wbSaver.save(wb, filePath)
        if saveRs.isOk():
            if isinstance(filePath, Path):
                wb.workbookKey = WorkbookKeyImp(wb.workbookKey.fileName, filePath)
            if isinstance(filePath, str):
                wb.workbookKey = WorkbookKeyImp(wb.workbookKey.fileName, Path(filePath))
            self.wbContainer.addWorkbook(wb)
        else:
            raise ValueError("Cannot save workbook at \"{v}\" to \"{p}\"".format(v=nameOrIndexOrKey, p=str(filePath)))

    # TODO test this
    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        wb = self.getWorkbook(nameOrIndexOrKey)
        if wb is not None:
            saveResult = self.__wbSaver.save(wb, wb.workbookKey.filePath)
            if saveResult.isErr():
                raise ValueError("Cannot save workbook at \"{v}\"".format(v=nameOrIndexOrKey))
        else:
            raise ValueError("Workbook at \"{v}\" does not exist".format(v=nameOrIndexOrKey))

    # TODO test this
    def loadWorkbook(self, filePath: str):
        loadResult: Result = self.__wbLoader.load(filePath)
        if loadResult.isOk():
            newWb: Workbook = loadResult.value()
            alreadyHasThisWorkbook = self.getWorkbook(newWb.workbookKey) is not None
            if alreadyHasThisWorkbook:
                print("Already load this workbook: \"{f}\"".format(f=filePath))
            else:
                self.wbContainer.addWorkbook(loadResult.value())
        else:
            raise ValueError("Can't load file: \"{f}\"".format(f=filePath))

    def __getWBOrRaiseError(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Workbook:
        wb = self.getWorkbook(nameOrIndexOrKey)
        if wb is not None:
            return wb
        else:
            raise ValueError("Workbook at \"{v}\" does not exist".format(v=nameOrIndexOrKey))
