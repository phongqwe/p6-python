

class SimpleScriptEntry:
    def __init__(self,name:str,script:str):
        self.script = script
        self.name = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, SimpleScriptEntry):
            return self.script == o.script and self.name == o.name
        else:
            return False

    def __hash__(self):
        return hash((self.name,self.script))

