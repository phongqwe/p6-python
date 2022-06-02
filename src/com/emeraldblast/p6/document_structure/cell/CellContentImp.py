from abc import ABC
from typing import Any

from com.emeraldblast.p6.document_structure.cell.CellContent import CellContent


class CellContentImp(CellContent):

    def __init__(self, value: Any | None, formula: str | None, script: str | None):
        self._script = script
        self._formula = formula
        self._value = value

    @property
    def value(self) -> Any | None:
        return self._value

    @property
    def formula(self) -> str | None:
        return self._formula

    @property
    def script(self) -> str | None:
        return self._script
