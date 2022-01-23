from bicp_document_structure.workbook.loader.WorkbookLoader import WorkbookLoader
from bicp_document_structure.workbook.loader.WorkbookLoaderStd import WorkbookLoaderStd


class WorkbookLoaders:
    __stdWbLoader = None

    @staticmethod
    def std() -> WorkbookLoader:
        if WorkbookLoaders.__stdWbLoader is None:
            WorkbookLoaders.__stdWbLoader = WorkbookLoaderStd()
        return WorkbookLoaders.__stdWbLoader