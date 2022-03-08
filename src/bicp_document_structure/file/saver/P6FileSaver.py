from abc import ABC
from pathlib import Path
from typing import Union

from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook


class P6FileSaver(ABC):
    """save a workbook to a file
    """

    def save(self, workbook: Workbook, filePath: Union[str,Path]) -> Result[None,ErrorReport]:
        """
        :param workbook:
        :param filePath:
        :return: a result indicate if this operation is a success or not 
        """
        raise NotImplementedError()
