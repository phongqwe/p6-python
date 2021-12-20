# from bicp_document_structure.app.UserFunctions import startApp, activeSheet, activeWorkbook


class A:
    def __init__(self):
        pass
    def scope(self):
        return globals()

class B:
    def __init__(self):
        pass

    @staticmethod
    def f1(): return 1

    @staticmethod
    def f2(): return 2


def main():
    z = B.__dict__
    for k,v in z.items():
        if isinstance(v,staticmethod):
            print(k)


if __name__ == "__main__":
    main()

