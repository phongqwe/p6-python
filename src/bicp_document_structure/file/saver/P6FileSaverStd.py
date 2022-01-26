from pathlib import Path
from typing import Union

from bicp_document_structure.file.P6File import P6File
from bicp_document_structure.file.P6Files import P6Files
from bicp_document_structure.file.saver.P6FileSaver import P6FileSaver
from bicp_document_structure.file.saver.P6FileSaverErrors import P6FileSaverErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook


class P6FileSaverStd(P6FileSaver):

    def save(self, workbook: Workbook, filePath: Union[str, Path, None]) -> Result:
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
                    ErrorReport(
                        header=P6FileSaverErrors.UnableToWriteFile.header,
                        data=P6FileSaverErrors.UnableToWriteFile.Data(
                            path,e
                        ),
                    )
                )
        except Exception as e:
            return Err(
                ErrorReport(
                    header=P6FileSaverErrors.UnableToAccessPath.header,
                    data=P6FileSaverErrors.UnableToAccessPath.Data(
                        path,e
                    ),
                )
            )