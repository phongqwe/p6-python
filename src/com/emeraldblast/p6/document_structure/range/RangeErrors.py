from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.ToException import ToException
from com.emeraldblast.p6.document_structure.util.ToRepStr import ToRepStr
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

RErr="RErr" #Range errors

class RangeErrors:
    class CellNotInRangeReport(ErrorReport):
        header = ErrorHeader(f"{RErr}0", "Cell not in range")

        class Data(ToRepStr, ToException):
            def __init__(self, cellAddress:CellAddress, rangeAddress:RangeAddress):
                self.rangeAddress = rangeAddress
                self.cellAddress = cellAddress

            def repStr(self) -> str:
                return f"cell with address {str(self.cellAddress)} is not in range {str(self.rangeAddress)}"

            def toException(self) -> Exception:
                return Exception(
                    self.repStr()
                )
        def __init__(self, cellAddress:CellAddress, rangeAddress:RangeAddress):
            super().__init__(
                RangeErrors.CellNotInRangeReport.header,
                RangeErrors.CellNotInRangeReport.Data(cellAddress, rangeAddress)
            )

