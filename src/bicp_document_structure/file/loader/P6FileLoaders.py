from bicp_document_structure.file.loader.P6FileLoader import P6FileLoader
from bicp_document_structure.file.loader.P6FileLoaderStd import P6FileLoaderStd


class P6FileLoaders:
    __stdWbLoader = None

    @staticmethod
    def standard() -> P6FileLoader:
        if P6FileLoaders.__stdWbLoader is None:
            P6FileLoaders.__stdWbLoader = P6FileLoaderStd()
        return P6FileLoaders.__stdWbLoader