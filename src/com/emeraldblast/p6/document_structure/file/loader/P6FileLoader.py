from abc import ABC
from pathlib import Path
from typing import Union

from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class P6FileLoader(ABC):
    """load a Workbook from a a file

    """
    def load(self,filePath:Union[str,Path])->Result[Workbook,ErrorReport]:
        """
        load a Workbook from a file
        :param filePath: path of workbook file
        :param onCellChange: a listener invoked when a cell is changed
        :return: a result indicate if this operation is a success or not
        """
        raise NotImplementedError()