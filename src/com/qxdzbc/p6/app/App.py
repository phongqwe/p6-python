from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any

from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class App(ABC):
    """
    this class represents the state of the app.
    """

    @property
    def workbooks(self) -> list[Workbook]:
        """return a list of all the currently opened workbooks"""
        raise NotImplementedError()

    def getRangeRs(self, rangeId: RangeId) -> Result[Range, ErrorReport]:
        raise NotImplementedError()

    def getWorksheetRs(self, workbookKey: WorkbookKey, worksheetName: str) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    @property
    def rootApp(self) -> 'App':
        raise NotImplementedError()

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        raise NotImplementedError()

    def setActiveWorkbook(self, wbKey: WorkbookKey):
        """
        Set workbook at indexOrName the active workbook.
        Should raise an exception if the indexOrName is invalid
        """
        raise NotImplementedError()

    def setActiveWorkbookRs(self, wbKey: WorkbookKey) -> Result[Workbook, ErrorReport]:
        """
        Set workbook at indexOrName the active workbook.
        :return a Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        """
        :return: the activesheet of the activebook.  The returned worksheet is connected to all the reactors of this app
        """
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int) -> Workbook:
        """:return workbook at an index. The returned workbook is connected to all the reactors of this app"""
        raise NotImplementedError()

    def getWorkbookByName(self, name: str) -> Workbook:
        """:return workbook at a name. The returned workbook is connected to all the reactors of this app"""
        raise NotImplementedError()

    def getWorkbookByKey(self, key: WorkbookKey) -> Workbook:
        """:return workbook at a key. The returned workbook is connected to all the reactors of this app"""
        raise NotImplementedError()

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Workbook:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app
        :raise exception if the workbook is unavailable
        """
        raise NotImplementedError()

    def getWorkbookOrNone(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app. Return none if the workbook is not available"""
        raise NotImplementedError()

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors/notifier of this app"""
        raise NotImplementedError()

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        """create a new workbook, and add it to this app """
        raise NotImplementedError()

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        """create a new workbook, and add it to this app 
        :return a Result object containinng the new workbook
        """
        raise NotImplementedError()

    def hasWorkbook(self, wbKey:WorkbookKey) -> bool:
        raise NotImplementedError()

    def closeWorkbookRs(self, keyOrNameOrIndex:Union[WorkbookKey,str,int])-> Result[WorkbookKey, ErrorReport]:
        """
        close a workbook
        :return a Result object containing the target workbook key
        """
        raise NotImplementedError()

    def closeWorkbook(self, keyOrNameOrIndex:Union[WorkbookKey,str,int])->WorkbookKey:
        """close a workbook or raise an exception if there's an error"""
        raise NotImplementedError()

    def closeWorkbookByWbKey(self, wbKey:WorkbookKey)->WorkbookKey:
        """close a workbook"""
        raise NotImplementedError()

    def closeWorkbookByWbKeyRs(self, wbKey:WorkbookKey) -> Result[WorkbookKey, ErrorReport]:
        """
        close a workbook
        :return a Result object containing the target workbook key
        """
        raise NotImplementedError()

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str, Path]):
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        """
        raise NotImplementedError()

    def saveWorkbookAtPathRs(self,
                             wbKey: WorkbookKey,
                             filePath: str | Path) -> Result[Workbook, ErrorReport]:
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        """
        raise NotImplementedError()

    def saveWorkbook(self, wbKey:WorkbookKey):
        """
        save a workbook at nameOrIndex
        """
        raise NotImplementedError()

    def saveWorkbookRs(self, wbKey:WorkbookKey) -> Result[Any, ErrorReport]:
        """
        save a workbook at nameOrIndex
        :return:
        """
        raise NotImplementedError()

    def loadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        """
        load a workbook from a file path, and add it to this app state
        because of the potential difference between file content and loaded content,
        if a workbook is already loaded, attempting loading it will return raise an exception.
        :param filePath:
        :return:
        """
        raise NotImplementedError()

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        Load a file using the default loader
        :param filePath:
        """

        raise NotImplementedError()

    def printWorkbookSummary(self):
        raise NotImplementedError()
