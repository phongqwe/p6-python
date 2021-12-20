from bicp_document_structure.app.Other import startApp, activeSheet, activeWorkbook


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
    # g = getGlobals()
    startApp()
    activeBook = activeWorkbook()
    activeBook.createNewSheet("Sheet1")
    activeBook.setActiveSheet("Sheet1")
    sheet = activeSheet()
    cell = sheet.cell((1,1))
    cell.code = "x=1;x+10"
    cell.runCode()
    print(cell.value)
    # print(g["__appInstances"])


if __name__ == "__main__":
    main()

