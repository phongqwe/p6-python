from bicp_document_structure.range.Range import Range


class WorksheetFunctions:
    @staticmethod
    def SUM(cellRange: Range)->float:
        rt = 0
        for cell in cellRange.cells:
            rt += cell.floatValue
        return rt

