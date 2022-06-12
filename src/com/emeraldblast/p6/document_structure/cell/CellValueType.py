from enum import Enum
from typing import Any

from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport


class CellValueType(Enum):
    FORMULA = 1
    BOOL = 2
    STR = 3
    INT = 4
    FLOAT = 5
    ERROR_REPORT = 6
    NOTHING = 7
    EXCEPTION = 8
    OBJ = 9

    @staticmethod
    def infer(obj: Any | None) -> 'CellValueType':
        if obj is None:
            return CellValueType.NOTHING
        else:
            if isinstance(obj, str):
                if CellUtils.isFormula(obj):
                    return CellValueType.FORMULA
                else:
                    return CellValueType.STR
            if isinstance(obj, bool):
                return CellValueType.BOOL
            if isinstance(obj, int):
                return CellValueType.INT
            if isinstance(obj, float):
                return CellValueType.FLOAT
            if isinstance(obj, Exception):
                return CellValueType.EXCEPTION
            if isinstance(obj, ErrorReport):
                return CellValueType.ERROR_REPORT

            return CellValueType.OBJ
