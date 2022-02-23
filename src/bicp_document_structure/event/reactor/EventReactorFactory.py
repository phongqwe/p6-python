import uuid
from typing import Callable

from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData


class EventReactorFactory:
    @staticmethod
    def makeCellReactor(callback:Callable[[CellEventData], None]):
        """create a cell reactor with randomize uuid4 id"""
        return CellReactor(str(uuid.uuid4()), callback)
