from abc import ABC

from bicp_document_structure.util.CanCheckEmpty import CanCheckEmpty


class WithSize(CanCheckEmpty, ABC):
    @property
    def size(self) -> int:
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        return self.size == 0
