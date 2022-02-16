
class P6Event:
    """
    Contain description of an event, serve as a tag of sort
    """
    def __init__(self, name:str,code:str):
        self._code = code
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self):
        return self._code

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, P6Event):
            return self.name == other.name
        else:
            return False
