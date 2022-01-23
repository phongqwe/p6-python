from pathlib import Path
from typing import Union

from bicp_document_structure.report.ReportJson import ReportJson
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.saver.WorkbookSaver import WorkbookSaver


class WorkbookSaverStd(WorkbookSaver):

    def save(self, workbook: Workbook, filePath: Union[str, Path]) -> Result:
        try:
            file = open(filePath, "w")
            try:
                file.write(str(workbook.toJson()))
                return Ok(ReportJson(
                    isOk=True,
                    message="",
                    data=None
                ))
            except:
                report = ReportJson(
                    isOk=False,
                    message="unable write file",
                    data={
                        "filePath": str(filePath),
                        "workBook": workbook.name
                    }
                )
                return Err(report)
        except:
            report = ReportJson(
                isOk=False,
                message="unable to access path: {}".format(str(filePath)),
                data={
                    "filePath": str(filePath),
                    "workBook": workbook.name
                }
            )
            return Err(report)
