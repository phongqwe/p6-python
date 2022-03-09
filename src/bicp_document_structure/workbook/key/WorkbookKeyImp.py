import os
from pathlib import Path
from typing import Optional

from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class WorkbookKeyImp(WorkbookKey):

    def __init__(self, fileName: str, filePath: Path | None = None):
        self.__filePath: Optional[Path] = filePath
        self.__fileName = fileName

    @staticmethod
    def fromPathStr(path: str):
        p = Path(path)
        fileName = os.path.basename(p)
        return WorkbookKeyImp(fileName, p)

    @property
    def filePath(self) -> Path:
        return self.__filePath

    @property
    def fileName(self) -> str:
        return self.__fileName
