from abc import ABC


class WithWorkbookData(ABC):
    @property
    def workbook(self):
        raise NotImplementedError()