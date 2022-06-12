import pyperclip

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.copy_paste.paster.BasePaster import BasePaster

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class TextPaster(BasePaster):
    def doPaste(self,anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        # the use of None in this function is exceptional, don't do it elsewhere.
        text = pyperclip.paste()
        if CellUtils.isFormula(text):
            cell = DataCell(
                address = CellAddresses.fromColRow(1,1),
                formula = text.strip(),
            )
        else:
            cell = DataCell(
                address = CellAddresses.fromColRow(1,1),
                value = text

            )
        return Ok(RangeCopy(
            rangeId = RangeId(
                # dummy range address
                rangeAddress =RangeAddresses.fromLabel("@A1:A1"),
                workbookKey = None,
                worksheetName = None,
            ),
            cells = [
                cell
            ]
        ))
