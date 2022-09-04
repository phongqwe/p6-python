from com.qxdzbc.p6.document_structure.range.Range import Range


class WorksheetFunctions:
    """Worksheet functions name must always be upper case"""
    @staticmethod
    def SUM(cellRange: Range)->float:
        rt = 0
        for cell in cellRange.cells:
            rt += cell.floatValue
        return rt

