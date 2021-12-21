from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class CellJson(dict):
    def __init__(self,value:str,code:str,address:CellAddressJson):
        super().__init__()
        self.value = value
        self.code = code
        self.addr = address
