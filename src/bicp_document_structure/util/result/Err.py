from bicp_document_structure.util.result.Result import Result


class Err(Result):

    def __init__(self, value):
        self.__value = value

    @property
    def err(self):
        return self.__value

    def value(self):
        return None

    def isOk(self):
        return False

    def isErr(self):
        return True