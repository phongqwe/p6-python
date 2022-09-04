import ast

import pyperclip
from com.qxdzbc.p6.document_structure.app.R import R

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.qxdzbc.p6.document_structure.copy_paste.CopyPasteErrors import CopyPasteErrors
from com.qxdzbc.p6.document_structure.copy_paste.paster.BasePaster import BasePaster
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result


class ProtoPaster(BasePaster):
    def doPaste(self,anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        protoBytesStr = pyperclip.paste()
        protoBytes = ast.literal_eval(protoBytesStr)
        o = RangeCopy.fromProtoBytes(protoBytes)

        colCount = o.rangeId.rangeAddress.colCount()
        rowCount = o.rangeId.rangeAddress.rowCount()

        remainingCol = R.WorksheetConsts.colLimit - anchorCell.colIndex + 1
        remainingRow = R.WorksheetConsts.rowLimit - anchorCell.rowIndex + 1

        if colCount > remainingCol or rowCount > remainingRow:
            return Err(CopyPasteErrors.CantPasteBecauseDataIsLargerThanDestinationRange.report(
                colCount, rowCount, remainingCol, remainingRow
            ))

        return Ok(o)
