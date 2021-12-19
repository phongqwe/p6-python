from bicp_document_structure.cell.address.CellAddress import CellAddress


class AddressTranslator:
    def translate(self, address)->CellAddress:
        """translate an address (whatever it is) into a CellAddress"""
        raise NotImplementedError()