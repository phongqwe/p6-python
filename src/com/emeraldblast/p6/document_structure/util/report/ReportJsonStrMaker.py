from abc import ABC


class ReportJsonStrMaker(ABC):
    """able to create a json string for reporting purposes"""
    def reportJsonStr(self)->str:
        raise NotImplementedError()