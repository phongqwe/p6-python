class ErrorHeader:
    def __init__(self,errorCode:str, errorDescription:str):
        self.errorCode = errorCode
        self.errorDescription =errorDescription

    def __str__(self) -> str:
        return"""
ErrorCode: {errorCode},
Description: {errorDescription}
""".format(errorCode=self.errorCode,errorDescription=self.errorDescription)