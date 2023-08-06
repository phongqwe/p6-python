from abc import ABC
from pathlib import Path
from typing import Tuple

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookKeyProto


class WorkbookKey(ToProto[WorkbookKeyProto],ABC):
    """
    An identifier class for identifying workbook.
    Each workbook as a unique WorkbookKey
    """

    def setPath(self,newPath:Path)->'WorkbookKey':
        raise NotImplementedError()

    def toProtoObj(self) -> WorkbookKeyProto:
        rt = WorkbookKeyProto()
        rt.name = self.fileName
        if self.filePath is not None:
            rt.path = str(self.filePath.absolute())
        return rt

    @property
    def filePath(self) -> Path:
        raise NotImplementedError()

    @property
    def fileName(self) -> str:
        raise NotImplementedError()

    def __key(self)->Tuple:
        p = None
        if self.filePath is not None:
            p = self.filePath.absolute()
        return p, self.fileName

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


