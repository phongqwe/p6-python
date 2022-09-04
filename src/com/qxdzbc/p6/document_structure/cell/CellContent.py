from abc import ABC
from typing import Any, Optional


class CellContent(ABC):
    @property
    def value(self) -> Any | None:
        raise NotImplementedError()

    @property
    def formula(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    def script(self) -> Optional[str]:
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other,CellContent):
            c1 = self.script == other.script
            c2 = self.value == other.value
            c3 = self.formula == other.formula
            return c1 and c2 and c3
        else:
            return False