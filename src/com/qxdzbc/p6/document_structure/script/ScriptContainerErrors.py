from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport

SCErrs = "BE_ScriptContainerErrors_"


class ScriptContainerErrors:
    class ScriptAlreadyExist:
        header = ErrorHeader(f"{SCErrs}0", f"script already exist")

        @staticmethod
        def report(scriptName: str) -> ErrorReport:
            header = ScriptContainerErrors.ScriptAlreadyExist.header.setDescription(
                f"script '{scriptName}' already exist")
            return ErrorReport(header = header)

    class MultipleScriptAlreadyExist:
        header = ErrorHeader(f"{SCErrs}1", f"multiple scripts already exist")

        @staticmethod
        def report(scriptNameList: list[str]) -> ErrorReport:
            header = ScriptContainerErrors.MultipleScriptAlreadyExist.header.setDescription(
                f"script '{scriptNameList}' already exist")
            return ErrorReport(header = header)
