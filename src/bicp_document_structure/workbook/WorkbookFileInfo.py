from pathlib import Path


class WorkbookFileInfo:
    def getFilePath(self)->Path:
        raise NotImplementedError()

    def getFileName(self)->str:
        raise NotImplementedError()
