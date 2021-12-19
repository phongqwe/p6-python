from bicp_document_structure.util.result.Result import Result


class WorkbookLoader:
    """load a Workbook from a a file"""
    def load(self,filePath:str)->Result:
        """
       load a Workbook from a a file
        :param filePath: path of workbook file
        :return: a result indicate if this operation is a success or not
        """
        raise NotImplementedError()