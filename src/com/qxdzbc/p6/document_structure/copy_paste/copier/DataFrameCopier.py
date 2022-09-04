import pandas

from com.qxdzbc.p6.document_structure.copy_paste.copier.BaseCopier import BaseCopier

from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.range.Range import Range



class DataFrameCopier(BaseCopier):
    def __init__(self, isCopyFull: bool = True, isCopySource:bool = True):

        self.isCopySource = isCopySource
        self.isCopyFull = isCopyFull

    def doCopy(self, rng: 'Range') -> Result[None, ErrorReport]:
        extractionFunction = None
        if self.isCopySource:
            extractionFunction = rng.toStrictSourceValueArray
            if self.isCopyFull:
                extractionFunction = rng.toFullSourceValueArray
        else:
            extractionFunction = rng.toStrictValueArray
            if self.isCopyFull:
                extractionFunction = rng.toFullValueArray

        df = pandas.DataFrame.from_records(extractionFunction())
        df.to_clipboard(excel = True, index = False, header = None)
        return Ok(None)
