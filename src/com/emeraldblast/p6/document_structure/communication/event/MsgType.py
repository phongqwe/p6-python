from enum import Enum


class MsgType(Enum):
    """
    @deprecated dont update this any further
    """
    CellUpdateValue= "cell_value_update"
    CellUpdateScript= "cell_update_script"
    CellUpdateFormula= "cell_update_formula"
    CellClearScriptResult= "cell_clear_script_result"

    ColReRun="col_rerun"
    RangeReRun="range_rerun"
    WorksheetReRun="worksheet_rerun"
    WorkbookReRun="workbook_rerun"

