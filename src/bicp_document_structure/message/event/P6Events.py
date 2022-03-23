from bicp_document_structure.message.event.data.RenameWorksheetOkData import RenameWorksheetOkData
from bicp_document_structure.message.proto.DocPM_pb2 import RenameWorksheetOkProto, WorkbookKeyProto
from bicp_document_structure.util.ToProto import ToProto, P

from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.MsgType import MsgType
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey

WSE = "WSE"
CE = "CE"
RE = "RE"
WBE = "WBE"
class P6Events:
    class Cell:
        UpdateValue = P6Event("Update cell value", f"{CE}0", MsgType.CellUpdateValue.value)
        UpdateScript = P6Event("Update cell script", f"{CE}1", MsgType.CellUpdateScript.value)
        UpdateFormula = P6Event("Update cell formula", f"{CE}2", MsgType.CellUpdateFormula.value)
        ClearScriptResult = P6Event("Clear cell script result", f"{CE}3", MsgType.CellClearScriptResult.value)

    class Worksheet:
        ReRun = P6Event("ReRun worksheet", f"{WSE}0", MsgType.WorksheetReRun.value)
        class RenameOk:
            event = P6Event("Rename worksheet ok", f"{WSE}1","worksheet_rename_ok")
            Data = RenameWorksheetOkData

        RenameFail = P6Event("Rename worksheet fail", f"{WSE}2","worksheet_rename_fail")

    class Range:
        ReRun = P6Event("ReRun range", f"{RE}0",MsgType.RangeReRun.value)

    class Workbook:
        ReRun = P6Event("ReRun workbook", f"{WBE}0",MsgType.WorkbookReRun.value)
        RemoveWorksheetOk = P6Event("Remove worksheet", f"{WBE}1","workbook_remove_worksheet_ok")
        RemoveWorksheetFail = P6Event("Remove worksheet", f"{WBE}2","workbook_remove_worksheet_fail")
