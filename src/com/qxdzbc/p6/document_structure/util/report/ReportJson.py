import json
from typing import Any

from com.qxdzbc.p6.document_structure.util.ToJson import ToJson
from com.qxdzbc.p6.document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result


class ReportJson(ToJson):

    def __init__(self, isOk: bool, message: str, data: str):
        """
        :param isOk:
        :param message:
        :param data: should be a json string
        """
        self.isOk = isOk
        self.message = message
        self.data = data

    @staticmethod
    def fromResultWithErrorReport(result: Result[Any, ErrorReport]):
        if result.isOk():
            data = result.value
            dataStr = ""
            if isinstance(data, ReportJsonStrMaker):
                dataStr = data.reportJsonStr()
            else:
                dataStr = str(data)
            return ReportJson(
                isOk = True,
                message = "Ok",
                data = dataStr
            )
        else:
            if isinstance(result.err, ErrorReport):
                errReport = result.err
                header = errReport.header
                dataJsonStr = ""
                if isinstance(errReport.data, ReportJsonStrMaker):
                    dataJsonStr = errReport.data.reportJsonStr()
                else:
                    dataJsonStr = str(errReport.data)
                return ReportJson(
                    isOk = False,
                    message = """{errorCode}: {errorDescription}""".format(errorCode = header.errorCode,
                                                                           errorDescription = header.errorDescription),
                    data = dataJsonStr
                )
            else:
                raise ValueError("err must be an ErrorReport")

    def __str__(self):
        return json.dumps(self.__dict__)

    def toJsonDict(self) -> dict:
        return self.__dict__
