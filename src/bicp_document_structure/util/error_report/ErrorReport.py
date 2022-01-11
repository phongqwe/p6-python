from bicp_document_structure.util.error_report.ErrorHeader import ErrorHeader


class ErrorReport:
    @property
    def header(self)->ErrorHeader:
        raise NotImplementedError()

    @property
    def data(self):
        raise NotImplementedError()