from typing import Optional, Union, Tuple

from com.qxdzbc.p6.app import App
from com.qxdzbc.p6.app.GlobalScope import getGlobals
from com.qxdzbc.p6.app.RpcApp import RpcApp
from com.qxdzbc.p6.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.di.Container import Container

"""
This module contains functions to be used by users to control the application.
"""
appKey = "__P6AppInstance"


def startApp():
    """create the app singleton"""
    g = getGlobals()
    if appKey not in g.keys():
        app = Container.rpcApp()
        g[appKey] = app


def stopApp():
    """ stop the app, clear everything """
    g = getGlobals()
    if appKey in g.keys():
        del g[appKey]


def restartApp():
    """restart the app"""
    stopApp()
    startApp()

def getApp() -> RpcApp:
    """get the singleton App instance"""
    startApp()
    g = getGlobals()
    return g[appKey]


def getActiveWorkbookRs() -> Optional[Workbook]:
    return getApp().activeWorkbook


def setActiveWorkbook(indexOrName):
    getApp().setActiveWorkbook(indexOrName)


def getActiveWorksheetRs() -> Optional[Worksheet]:
    wb = getActiveWorkbookRs()
    if wb is not None:
        return getActiveWorkbookRs().activeWorksheet
    else:
        return None


def setActiveSheet(indexOrName: Union[str, int]):
    wb: Optional[Workbook] = getActiveWorkbookRs()
    if wb is None:
        raise AppErrors.WorkbookNotExist.report(indexOrName).toException()

    wb.setActiveWorksheet(indexOrName)


def getWorksheetRs(nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
    wb = getActiveWorkbookRs()
    if wb is None:
        return None
    return wb.getWorksheet(nameOrIndex)


def getRange(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Optional[Range]:
    sheet = getActiveWorksheetRs()
    if sheet is None:
        return None
    return sheet.range(rangeAddress)


def cell(address: Union[str, CellAddress, Tuple[int, int]]) -> Optional[Cell]:
    """get a cell from the current active sheet"""
    sheet = getActiveWorksheetRs()
    if sheet is None:
        return None
    return sheet.getCell(address)

def getWorkbook(nameOrIndexOrKey: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
    app: App = getApp()
    wb = app.getWorkbook(nameOrIndexOrKey)
    return wb

def printWorkbookSummary():
    app = getApp()
    app.printWorkbookSummary()


def listWorksheet(workBookNameOrIndexOrKey: Union[str, int, WorkbookKey, None] = None) -> str:
    """list Worksheets of the active workbook"""
    if workBookNameOrIndexOrKey is None:
        wb = getActiveWorkbookRs()
    else:
        wb = getWorkbook(workBookNameOrIndexOrKey)
    if wb is not None:
        return wb.summary()
    else:
        return ""
