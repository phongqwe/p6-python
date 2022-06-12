import pandas

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.copy_paste.BasePaster import BasePaster
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class DataFramePaster(BasePaster):
    def doPaste(self) -> Result[RangeCopy, ErrorReport]:
        df = pandas.read_clipboard(header = None)
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

        return Ok(RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("@A1:A1"),
                workbookKey = None,
                worksheetName = None
            ),
            cells = cells
        ))
