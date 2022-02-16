from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.reactor.EventReactor import EventReactor, D

# todo implement this
class CellEventReactor(EventReactor[Cell]):
    @property
    def id(self) -> str:
        pass

    def react(self, data: D):
        pass