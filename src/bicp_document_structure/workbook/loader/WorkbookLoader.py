from abc import ABC

from bicp_document_structure.util.result.Result import Result


class WorkbookLoader(ABC):
    """load a Workbook from a a file
    TODO implement this

    """
    def load(self,filePath:str)->Result:
        """
       load a Workbook from a a file
        :param filePath: path of workbook file
        :return: a result indicate if this operation is a success or not
        """
        raise NotImplementedError()