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


def startApp():
    getApp()
    g = getGlobals()
    functionList = [
        getApp,

        getActiveWorkbook,
        setActiveWorkbook,

        getActiveSheet,
        setActiveSheet,

        getRange,
        getCell
    ]
    for f in functionList:
        g[f.__name__] = f

def getApp() -> App:
    """get the singleton App instance"""
    g = getGlobals()
    if "__appInstances" not in g.keys():
        g["__appInstances"] = SingleBookApp()
    return g["__appInstances"]

def getActiveWorkbook() -> Optional[Workbook]:
    return getApp().activeWorkbook

def setActiveWorkbook(indexOrName):
    getApp().setActiveWorkbook(indexOrName)

def getActiveSheet() -> Optional[Worksheet]:
    return getActiveWorkbook().activeSheet

def setActiveSheet(indexOrName: Union[str, int]):
    getActiveWorkbook().setActiveSheet(indexOrName)

def getRange(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
    return getActiveSheet().range(rangeAddress)

def getCell(address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
    """get a cell from the current active sheet"""
    return getActiveSheet().cell(address)