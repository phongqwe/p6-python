from bicp_document_structure.util.result.Result import Result


class Err(Result):

    def __init__(self, errReport):
        self.__errReport = errReport

    @property
    def err(self):
        return self.__errReport

    def value(self):
        return None

    def isOk(self):
        return False

    def isErr(self):
        return True