from abc import ABC
from pathlib import Path
from typing import Union, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class P6FileLoader(ABC):
    """load a Workbook from a a file

    """
    def load(self,filePath:Union[str,Path],
             onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] = None
             )->Result[Workbook,ErrorReport]:
        """
        load a Workbook from a file
        :param filePath: path of workbook file
        :param onCellChange: a listener invoked when a cell is changed
        :return: a result indicate if this operation is a success or not
        """
        raise NotImplementedError()