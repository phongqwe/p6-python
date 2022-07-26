from typing import Any, Optional

from com.emeraldblast.p6.document_structure.cell.CellContent import CellContent


class CellContentImp(CellContent):

    def __init__(self, value: Any | None, formula: Optional[str], script: Optional[str]):
        self._script = script
        self._formula = formula
        self._value = value

    @property
    def value(self) -> Any | None:
        return self._value

    @property
    def formula(self) -> Optional[str]:
        return self._formula

    @property
    def script(self) -> Optional[str]:
        return self._script
