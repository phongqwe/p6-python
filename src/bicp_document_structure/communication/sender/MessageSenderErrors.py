import json

from bicp_document_structure.communication.P6Message import P6Message
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader

errPrefix = "MessageSenderError "
class MessageSenderErrors:
    class FailToSend:
        header = ErrorHeader(errPrefix + "1", "fail to send message")

        class Data:
            def __init__(self, message:P6Message):
                self.message = message

            def __str__(self):
                return json.dumps({
                    "message":self.message.toJsonStr()
                })
    class WrongSocketType:
        header = ErrorHeader(errPrefix + "2", "wrong type of socket")

        class Data:
            def __init__(self, currentType,rightType):
                self.currentType = currentType
                self.rightType = rightType

            def __str__(self):
                return json.dumps({
                    "currentType":self.currentType,
                    "rightType":self.rightType,
                })