from abc import ABC

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy


class Paster(ABC):
    def pasteRange(self)->RangeCopy:
        raise NotImplementedError()