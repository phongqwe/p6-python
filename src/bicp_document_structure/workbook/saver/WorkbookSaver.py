from abc import ABC
from pathlib import Path
from typing import Union

from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookSaver(ABC):
    """save a workbook to a file
    TODO implement this
    """

    def save(self, workbook: Workbook, filePath: Union[str,Path]) -> Result:
        """
        :param workbook:
        :param filePath:
        :return: a result indicate if this operation is a success or not 
        """
        raise NotImplementedError()
