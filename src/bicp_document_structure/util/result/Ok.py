from bicp_document_structure.util.result.Result import Result


class Ok(Result):

    def __init__(self, value):
        self.__value = value

    @property
    def err(self):
        return None

    def value(self):
        return self.__value

    def isOk(self):
        return True

    def isErr(self):
        return False