from typing import Optional



class RpcInfo:
    def __init__(self, host:str, port:int):
        self._port:int = port
        self._host:Optional[str] = host

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port