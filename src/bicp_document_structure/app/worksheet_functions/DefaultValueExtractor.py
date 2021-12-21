from bicp_document_structure.cell.Cell import Cell


class DefaultValueExtractor:

    @staticmethod
    def str(cell:Cell)->str:
        cv = cell.value
        if cv is None or cv == "":
            pass
