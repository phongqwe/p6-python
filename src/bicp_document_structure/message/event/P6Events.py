from bicp_document_structure.message.event.data.CreateNewWorksheetData import CreateNewWorksheetData
from bicp_document_structure.message.event.data.RenameWorksheetOkData import RenameWorksheetOkData

from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.MsgType import MsgType

WSE = "WSE"
CE = "CE"
RE = "RE"
WBE = "WBE"
class P6Events:
    class Cell:
        class UpdateValue:
            event = P6Event(f"{CE}0", MsgType.CellUpdateValue.value)
        UpdateValueEvent = UpdateValue.event

        UpdateScript = P6Event(f"{CE}1", MsgType.CellUpdateScript.value)
        UpdateFormula = P6Event(f"{CE}2", MsgType.CellUpdateFormula.value)
        ClearScriptResult = P6Event(f"{CE}3", MsgType.CellClearScriptResult.value)

    class Worksheet:
        ReRun = P6Event(f"{WSE}0", MsgType.WorksheetReRun.value)
        class RenameOk:
            event = P6Event(f"{WSE}1","worksheet_rename_ok")
            Data = RenameWorksheetOkData

        RenameFail = P6Event(f"{WSE}2","worksheet_rename_fail")

    class Range:
        ReRun = P6Event(f"{RE}0",MsgType.RangeReRun.value)

    class Workbook:
        ReRun = P6Event(f"{WBE}0",MsgType.WorkbookReRun.value)
        RemoveWorksheetOk = P6Event(f"{WBE}1","workbook_remove_worksheet_ok")
        RemoveWorksheetFail = P6Event(f"{WBE}2","workbook_remove_worksheet_fail")
        class CreateNewWorksheet:
            event = P6Event(f"{WBE}3","create new worksheet")
            Data = CreateNewWorksheetData

