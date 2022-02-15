from typing import List


class RawMessage:
    def __init__(self, header: str, content: str):
        self.header: str = header
        self.content: str = content

    def toBytes(self) -> List[bytes]:
        rt = [
            bytes(self.header.encode("UTF-8")),
            bytes(self.content.encode("UTF-8")),
        ]
        return rt
