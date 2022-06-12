import pandas
from com.emeraldblast.p6.document_structure.app.R import R

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.copy_paste.CopyPasteErrors import CopyPasteErrors
from com.emeraldblast.p6.document_structure.copy_paste.paster.BasePaster import BasePaster
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class DataFramePaster(BasePaster):
    def doPaste(self,anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        df = pandas.read_clipboard(header = None,index_col=False)
        dimen = df.shape
        colCount = dimen[1]
        rowCount = dimen[0]

        remainingCol = R.WorksheetConsts.colLimit - anchorCell.colIndex + 1
        remainingRow = R.WorksheetConsts.rowLimit - anchorCell.rowIndex + 1

        if colCount > remainingCol or rowCount > remainingRow:
            return Err(CopyPasteErrors.CantPasteBecauseDataIsLargerThanDestinationRange.report(
                colCount,rowCount,remainingCol,remainingRow
            ))

        anchorCell = CellAddresses.fromColRow(1, 1)
        cells = []

        for rowIndex in range(len(df)):
            row = df.iloc[rowIndex]
            for colIndex in range(len(row)):
                content = df.iloc[rowIndex, colIndex]
                if not pandas.isna(content):
                    cellAddress = CellAddresses.fromColRow(
                        col = colIndex + anchorCell.colIndex,
                        row = rowIndex + anchorCell.rowIndex
                    )

                    isFormula = isinstance(content, str) and content.strip().startswith("=")

                    cell = None
                    if isFormula:
                        cell = DataCell(
                            address = cellAddress,
                            formula = content
                        )
                    else:
                        if isinstance(content,str):
                            cell = DataCell(
                                address = cellAddress,
                                value = CellUtils.parseValue(content)
                            )
                        else:
                            cell = DataCell(
                                address = cellAddress,
                                value = content
                            )

                    cells.append(cell)
        dimen = df.shape
        return Ok(RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.from2Cells(
                    firstCell = CellAddresses.fromColRow(1,1),
                    secondCell = CellAddresses.fromColRow(dimen[1], dimen[0])
                ),
                workbookKey = None,
                worksheetName = None
            ),
            cells = cells
        ))
