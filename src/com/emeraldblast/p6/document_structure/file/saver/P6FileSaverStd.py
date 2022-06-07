from pathlib import Path
from typing import Union

from com.emeraldblast.p6.document_structure.file.P6File import P6File
from com.emeraldblast.p6.document_structure.file.P6Files import P6Files
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaverErrors import P6FileSaverErrors
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class P6FileSaverStd(P6FileSaver):

    def saveRs(self, workbook: Workbook, filePath: Union[str, Path, None]) -> Result[None, ErrorReport]:
        path = filePath

        if filePath is None:
            path = workbook.workbookKey.filePath

        if path is None:
            path = P6Files.defaultPath

        try:
            file = open(filePath, 'w')
            try:
                jsonObject = workbook.toJson()
                fileObject = P6File(P6Files.currentVersion, jsonObject)
                file.write(str(fileObject))
                file.close()
                return Ok(None)
            except Exception as e:
                file.close()
                return Err(
                    P6FileSaverErrors.UnableToWriteFile.report(path, e)
                )
        except Exception as e:
            return Err(
                P6FileSaverErrors.UnableToAccessPath.report(path, e)
            )
