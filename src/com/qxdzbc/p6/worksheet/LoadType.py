from enum import Enum

from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import LoadDataRequestProto


class LoadType(Enum):

    OVERWRITE = 1
    KEEP_OLD_DATA_IF_COLLIDE = 2
    UNDEFINED = -1

    @staticmethod
    def fromProto(proto)->'LoadType':
        if proto == LoadDataRequestProto.LoadTypeProto.OVERWRITE:
            return LoadType.OVERWRITE

        if proto == LoadDataRequestProto.LoadTypeProto.KEEP_OLD_DATA_IF_COLLIDE:
            return LoadType.KEEP_OLD_DATA_IF_COLLIDE

        return LoadType.UNDEFINED

    def toProtoObj(self)->LoadDataRequestProto.LoadTypeProto:
        if self == LoadType.OVERWRITE:
            return LoadDataRequestProto.LoadTypeProto.OVERWRITE
        if self == LoadType.KEEP_OLD_DATA_IF_COLLIDE:
            return LoadDataRequestProto.LoadTypeProto.KEEP_OLD_DATA_IF_COLLIDE