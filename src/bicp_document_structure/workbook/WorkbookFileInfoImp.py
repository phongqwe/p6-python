import os
from pathlib import Path

from bicp_document_structure.workbook.WorkbookFileInfo import WorkbookFileInfo


class WorkbookFileInfoImp(WorkbookFileInfo):

    def __init__(self, filePath:Path, fileName:str):
        self.__filePath = filePath
        self.__fileName = fileName

    @staticmethod
    def fromPath(path:str):
        p = Path(path)
        fileName = os.path.basename(p)
        return WorkbookFileInfoImp(p,fileName)

    @property
    def filePath(self) -> Path:
        return self.__filePath

    @property
    def fileName(self) -> str:
        return self.__fileName