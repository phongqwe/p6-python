from abc import ABC


class CellContent(ABC):
    @property
    def value(self) -> str | None:
        raise NotImplementedError()

    @property
    def formula(self) -> str | None:
        raise NotImplementedError()

    @property
    def script(self) -> str | None:
        raise NotImplementedError()
