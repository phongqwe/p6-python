from pathlib import Path
from typing import Union

from bicp_document_structure.file.P6File import P6File
from bicp_document_structure.file.loader.P6FileLoader import P6FileLoader
from bicp_document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.Workbooks import Workbooks


class P6FileLoaderStd(P6FileLoader):
    def load(self, filePath: Union[str, Path]) -> Result:
        path = Path(filePath)
        if path.exists():
            try:
                file = open(path, "r")
                try:
                    fileContent = file.read()
                    p6File: P6File = P6File.fromJsonStr(fileContent)
                    workbook = Workbooks.wbFromJson(p6File.workbookJson, path)
                    file.close()
                    return Ok(workbook)
                except Exception as e:
                    file.close()
                    return Err(
                        ErrorReport(
                            header=P6FileLoaderErrors.UnableToReadFile.header,
                            data=P6FileLoaderErrors.UnableToReadFile.Data(path, e),
                            loc=""
                        )
                    )
            except Exception as e:
                return Err(
                    ErrorReport(
                        header=P6FileLoaderErrors.UnableToOpenFile.header,
                        data=P6FileLoaderErrors.UnableToOpenFile.Data(filePath, e),
                        loc=""
                    )
                )
        else:
            return Err(
                ErrorReport(
                    header=P6FileLoaderErrors.FileNotExist.header,
                    data=P6FileLoaderErrors.FileNotExist.Data(filePath, None),
                    loc=""
                )
            )

