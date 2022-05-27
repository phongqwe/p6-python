import json

from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

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

        def __init__(self, message: str):
            super().__init__(
                MessageSenderErrors.FailToSend.header,
                MessageSenderErrors.FailToSend.Data(message)
            )

    class WrongSocketType:
        header = ErrorHeader(errPrefix + "2", "wrong type of socket")

        class Data:
            def __init__(self, currentType, rightType):
                self.currentType = currentType
                self.rightType = rightType

            def __str__(self):
                return json.dumps({
                    "currentType": self.currentType,
                    "rightType": self.rightType,
                })
