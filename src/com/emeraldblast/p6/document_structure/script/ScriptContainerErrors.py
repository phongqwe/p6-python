from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

SCErrs = "BE_ScriptContainerErrors_"
class ScriptContainerErrors:
    class ScriptAlreadyExist:
        header = ErrorHeader(f"{SCErrs}0", f"script already exist")
        @staticmethod
        def report(scriptName:str)->ErrorReport:
            header = ScriptContainerErrors.ScriptAlreadyExist.header.updateDescription(f"script '{scriptName}' already exist")
            return ErrorReport(
                header=header
            )