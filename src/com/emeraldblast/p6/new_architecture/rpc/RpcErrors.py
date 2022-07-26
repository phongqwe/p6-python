from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

prefix = "Python_RpcErrors_"


class RpcErrors:
    class RpcServerIsDown:
        header = ErrorHeader(prefix + "1", "p6 rpc server is not up.")

        @staticmethod
        def report(detail: str = ""):
            return ErrorReport(
                header = RpcErrors.RpcServerIsDown.header.setDescription(detail),
            )
