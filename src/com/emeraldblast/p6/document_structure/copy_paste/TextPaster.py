import pyperclip

from com.emeraldblast.p6.document_structure.copy_paste.BasePaster import BasePaster

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class TextPaster(BasePaster):
    def doPaste(self) -> Result[RangeCopy, ErrorReport]:
        # the use of None in this function is exceptional, don't do it elsewhere.
        text = pyperclip.paste()
        if CellUtils.isFormula(text):
            cell = DataCell(
                address = None,
                formula = text.strip(),
            )
        else:
            cell = DataCell(
                address = None,
                value = text

            )
        return Ok(RangeCopy(
            rangeId = None,
            cells = [
                cell
            ]
        ))
