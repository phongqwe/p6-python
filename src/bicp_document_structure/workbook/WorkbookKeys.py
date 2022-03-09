from pathlib import Path

from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp


class WorkbookKeys:
    @staticmethod
    def fromPathStr(path: str) -> WorkbookKey:
        return WorkbookKeyImp.fromPathStr(path)

    @staticmethod
    def fromNameAndPath(name: str, path: str | Path | None) -> WorkbookKey:
        p = path
        if path is not None:
            if isinstance(path, str):
                p = Path(path)
        return WorkbookKeyImp(name, p)
