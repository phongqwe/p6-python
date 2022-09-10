from abc import ABC

from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty


class WithSize(CanCheckEmpty, ABC):
    @property
    def size(self) -> int:
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        return self.size == 0
