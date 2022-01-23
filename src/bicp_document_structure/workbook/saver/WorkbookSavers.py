from bicp_document_structure.workbook.saver.WorkbookSaver import WorkbookSaver
from bicp_document_structure.workbook.saver.WorkbookSaverStd import WorkbookSaverStd


class WorkbookSavers:
    __stdSaver = None

    @staticmethod
    def standard() -> WorkbookSaver:
        if WorkbookSavers.__stdSaver is None:
            WorkbookSavers.__stdSaver = WorkbookSaverStd()
        return WorkbookSavers.__stdSaver
