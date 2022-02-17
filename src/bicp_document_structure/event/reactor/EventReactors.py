import uuid
from typing import Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.reactor.cell.CellEventReactor import CellEventReactor


class EventReactors:
    @staticmethod
    def cellReactor(callback:Callable[[Cell],None]):
        """create a reactor with randomize uuid4 id"""
        return CellEventReactor(str(uuid.uuid4()), callback)
