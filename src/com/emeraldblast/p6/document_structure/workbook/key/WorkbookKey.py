from abc import ABC
from pathlib import Path
from typing import Tuple

from google.protobuf.struct_pb2 import NullValue

from com.emeraldblast.p6.proto.CommonProtos_pb2 import NullableString

from com.emeraldblast.p6.proto.DocProtos_pb2 import WorkbookKeyProto
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto


class WorkbookKey(ToProto[WorkbookKeyProto],ABC):
    """
    An identifier class for identifying workbook.
    Each workbook as a unique WorkbookKey
    """

    def toProtoObj(self) -> WorkbookKeyProto:
        rt = WorkbookKeyProto()
        rt.name = self.fileName
        pathStr = NullableString()
        if self.filePath is None:
            pathStr.null = NullValue.NULL_VALUE
        else:
            pathStr.str = str(self.filePath.absolute())
        rt.path.CopyFrom(pathStr)
        return rt

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


