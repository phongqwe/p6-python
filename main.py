from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.report.error.ErrorReports import ErrorReports


class A:
    def __init__(self):
        pass
    def z(self):
        return 100
if __name__ == "__main__":
    e = ErrorReports.toException(
        ErrorReport(
            header=AppErrors.WorkbookNotExist.header,
            data=AppErrors.WorkbookNotExist.Data(1)
        )
    )
    print(e)