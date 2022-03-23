
class P6Event:
    """
        P6Event needs to be this complex because in the future, there will be a needed for coded events
    """
    def __init__(self, description:str, code:str, msgRepresentation:str= ""):
        self._code = code
        self._name = description
        self._msgRepresentation = msgRepresentation

    @property
    def msgRepresentation(self):
        return self._msgRepresentation

    @property
    def description(self) -> str:
        return self._name

    @property
    def code(self):
        return self._code

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, P6Event):
            return self.code == other.code
        else:
            return False
