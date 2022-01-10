from enum import Enum


class CellMutationEvent(Enum):
    NEW_SCRIPT = 0
    NEW_VALUE = 1
    FORMAT_CHANGE = 2
    DELETED = 3
