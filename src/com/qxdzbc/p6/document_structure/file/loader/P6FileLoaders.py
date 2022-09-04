from com.qxdzbc.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.qxdzbc.p6.document_structure.file.loader.P6FileLoaderStd import P6FileLoaderStd
from com.qxdzbc.p6.document_structure.file.loader.P6ProtoFileLoader import P6ProtoFileLoader


class P6FileLoaders:

    __stdWbLoader = None
    @staticmethod
    def standard() -> P6FileLoader:
        if P6FileLoaders.__stdWbLoader is None:
            P6FileLoaders.__stdWbLoader = P6FileLoaderStd()
        return P6FileLoaders.__stdWbLoader

    __protoLoader = None
    @staticmethod
    def proto()->P6FileLoader:
        if P6FileLoaders.__protoLoader is None:
            P6FileLoaders.__protoLoader = P6ProtoFileLoader()
        return P6FileLoaders.__protoLoader