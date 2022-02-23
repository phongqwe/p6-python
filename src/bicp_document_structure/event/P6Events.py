from bicp_document_structure.event.P6Event import P6Event


class P6Events:
    class Cell:
        __prefix = "CE_"
        UpdateValue = P6Event("Update cell value", f"{__prefix}0")
        UpdateScript = P6Event("Update cell script", f"{__prefix}1")
        UpdateFormula = P6Event("Update cell formula", f"{__prefix}2")
        ClearScriptResult = P6Event("Clear cell script result", f"{__prefix}3")



    class Worksheet:
        __prefix = "WSE"
        ReRun = P6Event("ReRun worksheet",f"{__prefix}0")

    class Range:
        __prefix = "RE"
        ReRun = P6Event("ReRun range",f"{__prefix}0")

    class Column:
        __prefix = "CE"
        ReRun = P6Event("ReRun column", f"{__prefix}0")
    class Workbook:
        __prefix = "WBE"
        ReRun = P6Event("ReRun workbook",f"{__prefix}0")