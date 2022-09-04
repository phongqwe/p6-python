from com.qxdzbc.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.qxdzbc.p6.document_structure.file.saver.P6FileSaverStd import P6FileSaverStd
from com.qxdzbc.p6.document_structure.file.saver.P6ProtoFileSaver import P6ProtoFileSaver


class P6FileSavers:

    __stdSaver = None
    @staticmethod
    def standard() -> P6FileSaver:
        if P6FileSavers.__stdSaver is None:
            P6FileSavers.__stdSaver = P6FileSaverStd()
        return P6FileSavers.__stdSaver

    __protoSaver = None
    @staticmethod
    def proto()->P6FileSaver:
        if P6FileSavers.__protoSaver is None:
            P6FileSavers.__protoSaver = P6ProtoFileSaver()
        return P6FileSavers.__protoSaver
