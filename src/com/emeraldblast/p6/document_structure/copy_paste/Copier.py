from abc import ABC

from com.emeraldblast.p6.document_structure.range.Range import Range


class Copier(ABC):
    def copyRangeToClipboard(self,rng:Range):
        raise NotImplementedError()