from com.emeraldblast.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse


class CellMultiUpdateResponse(WorkbookUpdateCommonResponse,ToEventData):
    pass