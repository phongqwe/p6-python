from typing import Optional, Union, Tuple

from bicp_document_structure.app import App
from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.app.SingleBookApp import SingleBookApp
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


def getApp() -> App:
    g = getGlobals()
    if "__appInstances" not in g.keys():
        g["__appInstances"] = SingleBookApp()
    return g["__appInstances"]

def startApp():
    getApp()
    g = getGlobals()
    # add user functions to global scope
    g[getApp.__name__] = getApp
    g[activeWorkbook.__name__]= activeWorkbook
    g[setActiveWorkbook.__name__] = setActiveWorkbook
    g[activeSheet.__name__] = activeSheet
    g[setActiveSheet.__name__] = setActiveSheet
    g[getRange.__name__] = getRange
    g[cell.__name__] = cell


def activeWorkbook() -> Optional[Workbook]:
    return getApp().activeWorkbook


def setActiveWorkbook(indexOrName):
    getApp().setActiveWorkbook(indexOrName)


def activeSheet() -> Optional[Worksheet]:
    return activeWorkbook().activeSheet


def setActiveSheet(indexOrName: Union[str, int]):
    activeWorkbook().setActiveSheet(indexOrName)


def getRange(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
    return activeSheet().range(rangeAddress)


def cell(address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
    return activeSheet().cell(address)

# """
#     @A2
#     x = getRange("A1").value
#     y = getRange("A2").value
#     x+y
# """
# def runCode(cell: Cell, code: str):
#     cell.setCodeAndRun(code, getGlobals())
