from bicp_document_structure.util.ToJson import ToJson


class ErrorHeader(ToJson):
    def toJsonDict(self) -> dict:
        return self.__dict__

    def __init__(self,errorCode:str, errorDescription:str):
        self.errorCode = errorCode
        self.errorDescription =errorDescription

    def __str__(self) -> str:
        return"""
ErrorCode: {errorCode},
Description: {errorDescription}
""".format(errorCode=self.errorCode,errorDescription=self.errorDescription)