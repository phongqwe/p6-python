from bicp_document_structure.cell.address.CellIndex import CellIndex


class A:
    def __init__(self):
        pass
    def scope(self):
        return globals()

class B:
    def __init__(self):
        pass
    def scope(self):
        return globals()

def main():
    """
    calling globals from different file produce different objects
    so it is crucial that I give each cell the correct global scope

    code executor require a global and local scope because: it may access global var (such as app, workbook). It needs to know where to get them.
    :return:
    """
    a = A()
    b = B()
    c = CellIndex(1,1)
    print(a.scope() == c.scope()) #False


if __name__ == "__main__":
    main()

