from bicp_document_structure.range.Range import Range


class WorksheetFunctions:
    @staticmethod
    def sum(cellRange: Range):
        rt = 0
        for cell in cellRange.cells:
            # print(cell.code)
            rt += cell.numericValue
        return rt
