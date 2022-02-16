import json

from bicp_document_structure.message.P6Message import P6Message
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
