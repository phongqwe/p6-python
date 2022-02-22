import uuid
from typing import Callable

from bicp_document_structure.event.reactor.CellEventReactor import CellEventReactor
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData


class EventReactors:
    @staticmethod
    def makeCellReactor(callback:Callable[[CellEventData], None]):
        """create a reactor with randomize uuid4 id"""
        return CellEventReactor(str(uuid.uuid4()), callback)
