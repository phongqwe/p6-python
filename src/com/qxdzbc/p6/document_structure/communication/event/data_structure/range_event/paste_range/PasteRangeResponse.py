from com.qxdzbc.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData

from com.qxdzbc.p6.document_structure.communication.event.data_structure.ToP6Response import ToP6Response
from com.qxdzbc.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse


class PasteRangeResponse(ToEventData, WorkbookUpdateCommonResponse):
    pass
