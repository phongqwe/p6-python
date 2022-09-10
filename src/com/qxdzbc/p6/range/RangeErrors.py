from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.ToException import ToException
from com.qxdzbc.p6.util.ToRepStr import ToRepStr
from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

RErr="BE_RangeErrors_" #Range errors

class RangeErrors:
    class CellNotInRangeReport:
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
        @staticmethod
        def report(cellAddress:CellAddress, rangeAddress:RangeAddress):
            data = RangeErrors.CellNotInRangeReport.Data(cellAddress, rangeAddress)
            return ErrorReport(
                RangeErrors.CellNotInRangeReport.header.setDescription(f"{data.repStr()}"),
                data = data
            )


