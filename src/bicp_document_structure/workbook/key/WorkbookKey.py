from abc import ABC
from pathlib import Path
from typing import Tuple


class WorkbookKey(ABC):
    """
    An identifier class for identifying workbook.
    Each workbook as a unique WorkbookKey
    """
    @property
    def filePath(self) -> Path:
        raise NotImplementedError()

    @property
    def fileName(self) -> str:
        raise NotImplementedError()

    def __key(self)->Tuple:
        return self.filePath, self.fileName

    def __eq__(self, o: object) -> bool:
        if isinstance(o, WorkbookKey):
            return self.__key() == o.__key()
        else:
            return False

    def __hash__(self):
        return hash(self.__key())

    def __str__(self) -> str:
        return "name:{n}\npath:{p}".format(
            n=self.fileName,
            p=str(self.filePath)
        )


