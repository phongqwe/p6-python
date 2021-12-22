import os
from pathlib import Path
from typing import Optional

from bicp_document_structure.workbook.WorkbookFileInfo import WorkbookFileInfo


class WorkbookFileInfoImp(WorkbookFileInfo):

    def __init__(self, fileName: str, filePath: Optional[Path] = None):
        self.__filePath: Optional[Path] = filePath
        self.__fileName = fileName

    @staticmethod
    def fromPath(path: str):
        p = Path(path)
        fileName = os.path.basename(p)
        return WorkbookFileInfoImp(fileName, p)

    @property
    def filePath(self) -> Path:
        return self.__filePath

    @property
    def fileName(self) -> str:
        return self.__fileName
