"""
Global scope hold:
- app instances
- all the function that user can use directly to query the active objects:
    + getRange() => get some range from the active sheet
    + activeSheet() => get active sheet
    + activeWorkbook() => get active workbook
    + cell() => get a cell from the active sheet
    + runCode() => run code in a cell
- when user have a Cell object:
    + to run code: cell.runCode("code",globalScope) => this sig require a scope object. How do I turn it into: cell.runCode("code"). I can run getGlobals() inside runCode to get the default global scope. This will:
    import the globalscope into DataCell.
"""


def getGlobals():
    return globals()