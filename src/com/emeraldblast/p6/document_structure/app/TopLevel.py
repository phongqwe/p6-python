from typing import Optional, Union, Tuple

from com.emeraldblast.p6.document_structure.app import App
from com.emeraldblast.p6.document_structure.app.AppImp import AppImp
from com.emeraldblast.p6.document_structure.app.EventApp import EventApp
from com.emeraldblast.p6.document_structure.app.GlobalScope import getGlobals
from com.emeraldblast.p6.document_structure.app.errors.AppErrors import AppErrors
from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet

"""
This module contains functions to be used by users to control the application.
"""
appKey = "__P6AppInstance"


def startApp():
    """create the app singleton"""
    getApp()


def stopApp():
    """ stop the app, clear everything """
    g = getGlobals()
    if appKey in g.keys():
        del g[appKey]


def restartApp():
    """restart the app"""
    stopApp()
    startApp()


def getApp() -> App:
    """get the singleton App instance"""
    g = getGlobals()
    if appKey not in g.keys():
        app0 = AppImp()
        app = EventApp.create(
            app0,app0.eventNotifierContainer
        )
        g[appKey] = app
    return g[appKey]


def getActiveWorkbook() -> Workbook | None:
    return getApp().activeWorkbook


def setActiveWorkbook(indexOrName):
    getApp().setActiveWorkbook(indexOrName)


def getActiveSheet() -> Optional[Worksheet]:
    wb = getActiveWorkbook()
    if wb is not None:
        return getActiveWorkbook().activeWorksheet
    else:
        return None


def setActiveSheet(indexOrName: Union[str, int]):
    wb: Optional[Workbook] = getActiveWorkbook()
    if wb is None:
        raise AppErrors.WorkbookNotExist.report(indexOrName).toException()

    wb.setActiveWorksheet(indexOrName)


def getWorksheet(nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
    wb = getActiveWorkbook()
    if wb is None:
        return None
    return wb.getWorksheet(nameOrIndex)


def getRange(rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Optional[Range]:
    sheet = getActiveSheet()
    if sheet is None:
        return None
    return sheet.range(rangeAddress)


def cell(address: Union[str, CellAddress, Tuple[int, int]]) -> Optional[Cell]:
    """get a cell from the current active sheet"""
    sheet = getActiveSheet()
    if sheet is None:
        return None
    return sheet.cell(address)


def getWorkbook(nameOrIndexOrKey: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
    app: App = getApp()
    wb = app.getWorkbook(nameOrIndexOrKey)
    return wb


def listWorkbook():
    app = getApp()
    app.listWorkbook()


def listWorksheet(workBookNameOrIndexOrKey: Union[str, int, WorkbookKey, None] = None) -> str:
    """list Worksheets of the active workbook"""
    if workBookNameOrIndexOrKey is None:
        wb = getActiveWorkbook()
    else:
        wb = getWorkbook(workBookNameOrIndexOrKey)
    if wb is not None:
        return wb.summary()
    else:
        return ""
