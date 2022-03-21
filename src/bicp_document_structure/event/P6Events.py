from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.message.MsgType import MsgType


class P6Events:
    class Cell:
        __prefix = "CE_"
        UpdateValue = P6Event("Update cell value", f"{__prefix}0", MsgType.CellUpdateValue.value)
        UpdateScript = P6Event("Update cell script", f"{__prefix}1", MsgType.CellUpdateScript.value)
        UpdateFormula = P6Event("Update cell formula", f"{__prefix}2", MsgType.CellUpdateFormula.value)
        ClearScriptResult = P6Event("Clear cell script result", f"{__prefix}3", MsgType.CellClearScriptResult.value)

    class Worksheet:
        __prefix = "WSE"
        ReRun = P6Event("ReRun worksheet", f"{__prefix}0", MsgType.WorksheetReRun.value)
        RenameOk = P6Event("Rename worksheet ok", f"{__prefix}1","worksheet_rename_ok")
        RenameFail = P6Event("Rename worksheet fail", f"{__prefix}2","worksheet_rename_fail")

    class Range:
        __prefix = "RE"
        ReRun = P6Event("ReRun range", f"{__prefix}0",MsgType.RangeReRun.value)

    class Column:
        __prefix = "CE"
        ReRun = P6Event("ReRun column", f"{__prefix}0")

    class Workbook:
        __prefix = "WBE"
        ReRun = P6Event("ReRun workbook", f"{__prefix}0",MsgType.WorkbookReRun.value)
        RemoveWorksheetOk = P6Event("Remove worksheet", f"{__prefix}1","workbook_remove_worksheet_ok")
        RemoveWorksheetFail = P6Event("Remove worksheet", f"{__prefix}2","workbook_remove_worksheet_fail")
