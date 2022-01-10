from typing import Tuple



class CellJson(dict):
    """
    Json representation of a cell
    """
    def __init__(self,value:str,script:str,address:Tuple[int, int]):
        super().__init__()
        self.value = value
        self.script = script
        self.addr = address
