from collections import OrderedDict as ODict
from typing import Optional, OrderedDict, Union

from bicp_document_structure.app.App import App
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.workbook.WorkBook import Workbook


class AppImp(App):

    """
    Standard implementation of App interface
    TODO implement this
    """

    def __init__(self, workbookDict=None):

        if workbookDict is None:
            workbookDict = ODict()
        else:
            typeCheck(workbookDict, "workbookDick", OrderedDict)

        self.__workbookDict = workbookDict
        self.__activeWorkbook = None

    ### >> App << ###

    def hasNoWorkbook(self) -> bool:
        return len(self.__workbookDict) == 0

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        if self.__activeWorkbook is None:
            if self.hasNoWorkbook():
                return None
            else:
                self.__activeWorkbook = self.__workbookDict.values()[0]
                return self.__activeWorkbook
        else:
            return self.__activeWorkbook

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        return super().getWorkbookByIndex(index)

    def setActiveWorkbook(self, indexOrName: Union[int, str]):
        pass
