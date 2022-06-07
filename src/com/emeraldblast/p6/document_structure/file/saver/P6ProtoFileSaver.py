import time
from pathlib import Path

from com.emeraldblast.p6.document_structure.file.P6File2 import P6File2
from com.emeraldblast.p6.document_structure.file.P6FileContent import P6FileContent
from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaverErrors import P6FileSaverErrors
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class P6ProtoFileSaver(P6FileSaver):
    @property
    def rootSaver(self) -> 'P6FileSaver':
        return self

    def saveRs(self, workbook: Workbook, filePath: str | Path | None) -> Result[None, ErrorReport]:
        path = filePath

        if path:
            pass
        else:
            return Err(
                P6FileSaverErrors.InvalidPath.report(workbook.workbookKey)
            )

        wb = workbook.makeSavableCopy()

        meta = P6FileMetaInfo(date = time.time())
        fileContent = P6FileContent(
            meta = meta,
            wb = wb
        )
        p6FileProtoBytes = P6File2(
            version = "v1",
            content = fileContent.toProtoBytes()
        ).toProtoBytes()

        try:
            file = open(filePath, 'wb')
            try:
                file.write(p6FileProtoBytes)
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
