from pathlib import Path
from typing import Union

from com.emeraldblast.p6.document_structure.file.P6File2 import P6File2
from com.emeraldblast.p6.document_structure.file.P6FileContent import P6FileContent
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class P6ProtoFileLoader(P6FileLoader):
    @property
    def rootLoader(self) -> 'P6FileLoader':
        return self

    def loadRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        path = Path(filePath)
        if path.exists():
            try:
                file = open(path, "rb")
                try:
                    fileContent = file.read()
                    p6File: P6File2 = P6File2.fromProtoBytes(fileContent)
                    fileContent = P6FileContent.fromProtoBytes(p6File.content,filePath)
                    workbook = fileContent.wb
                    file.close()
                    workbookKey = WorkbookKeys.fromNameAndPath(path.name, path)
                    workbook.workbookKey = workbookKey
                    return Ok(workbook)
                except Exception as e:
                    file.close()
                    return Err(
                        ErrorReport(
                            header = P6FileLoaderErrors.UnableToReadFile.header,
                            data = P6FileLoaderErrors.UnableToReadFile.Data(path, e),
                        )
                    )
            except Exception as e:
                return Err(
                    ErrorReport(
                        header = P6FileLoaderErrors.UnableToOpenFile.header,
                        data = P6FileLoaderErrors.UnableToOpenFile.Data(filePath, e),
                    )
                )
        else:
            return Err(
                ErrorReport(
                    header = P6FileLoaderErrors.FileNotExist.header,
                    data = P6FileLoaderErrors.FileNotExist.Data(filePath, None),
                )
            )