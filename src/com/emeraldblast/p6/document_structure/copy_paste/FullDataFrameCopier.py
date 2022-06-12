import pandas

from com.emeraldblast.p6.document_structure.copy_paste.BaseCopier import BaseCopier
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class FullDataFrameCopier(BaseCopier):
    def doCopy(self, rng: Range) -> Result[None, ErrorReport]:
        df = pandas.DataFrame.from_records(rng.toFullSourceValueArray())
        df.to_clipboard(excel = True, index = False, header = None)
        return Ok(None)