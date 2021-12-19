from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookSaver:
    """save a workbook to a file"""

    def save(self,worbook:Workbook, filePath:str)->Result:
        """
        :param worbook:
        :param filePath:
        :return: a result indicate if this operation is a success or not 
        """
        raise NotImplementedError()