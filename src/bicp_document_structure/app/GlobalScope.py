"""
Global scope hold:
- app instances
- all the functions that user can use directly to query the active objects:
    + getRange() => get some range from the active sheet
    + activeSheet() => get active sheet
    + activeWorkbook() => get active workbook
    + cell() => get a cell from the active sheet
    + runCode() => run code in a cell
"""

def getGlobals():
    return globals()