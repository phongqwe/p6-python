from abc import ABC
from pathlib import Path
from typing import Union

from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook


class P6FileLoader(ABC):
    """load a Workbook from a a file
    TODO implement this

    """
    def load(self,filePath:Union[str,Path])->Result[Workbook,ErrorReport]:
        """
       load a Workbook from a a file
        :param filePath: path of workbook file
        :return: a result indicate if this operation is a success or not
        """
        raise NotImplementedError()