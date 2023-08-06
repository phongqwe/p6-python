import json

from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

errPrefix = "BE_MessageSenderErrors_"  # message sender error


class MessageSenderErrors:
    class FailToSend(ErrorReport):
        header = ErrorHeader(f"{errPrefix}1", "fail to send message")

        class Data:
            def __init__(self, message: str):
                self.message = message

            def __str__(self):
                return json.dumps({
                    "message": self.message
                })

        @staticmethod
        def report(message: str):
            data = MessageSenderErrors.FailToSend.Data(message)
            return ErrorReport(
                header = MessageSenderErrors.FailToSend.header.concatDescription(f"\n{str(data)}"),
                data = data
            )

    class WrongSocketType:
        header = ErrorHeader(errPrefix + "2", "wrong type of socket")

        class Data:
            def __init__(self, currentType, rightType):
                self.currentType = currentType
                self.rightType = rightType

            def __str__(self):
                rt = f"current type: {self.currentType}\nright type: {self.rightType}"
                return rt

        @staticmethod
        def report(currentType, rightType):
            data = MessageSenderErrors.WrongSocketType.Data(currentType, rightType)
            return ErrorReport(
                header = MessageSenderErrors.WrongSocketType.header.concatDescription(f"\n{str(data)}"),
                data = data
            )
