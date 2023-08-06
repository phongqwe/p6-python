

class ErrorHeader:

    def __init__(self,errorCode:str, errorDescription:str):
        self.errorCode = errorCode
        self.errorDescription =errorDescription

    def __str__(self) -> str:
        return"""
ErrorCode: {errorCode},
Description: {errorDescription}
""".format(errorCode=self.errorCode,errorDescription=self.errorDescription)

    def __eq__(self, other):
        if isinstance(other,ErrorHeader):
            return self.errorCode == other.errorCode
        else:
            return False

    def setDescription(self, newDescription:str)-> 'ErrorHeader':
        return ErrorHeader(
            errorCode = self.errorCode,
            errorDescription = newDescription
        )

    def concatDescription(self,newDescription:str)->'ErrorHeader':
        return ErrorHeader(
            errorCode = self.errorCode,
            errorDescription = self.errorDescription+newDescription
        )