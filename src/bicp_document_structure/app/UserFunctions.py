from typing import Optional, Union, Tuple

from bicp_document_structure.app import App
from bicp_document_structure.app.AppImp import AppImp
from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.report.error.ErrorReports import ErrorReports
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet

"""
This module contains functions to be used by users to control the application.
"""
appKey = "__appInstance"


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
        g[appKey] = AppImp()
    return g[appKey]


def getActiveWorkbook() -> Optional[Workbook]:
    return getApp().activeWorkbook


def setActiveWorkbook(indexOrName):
    getApp().setActiveWorkbook(indexOrName)


def getActiveSheet() -> Optional[Worksheet]:
    wb = getActiveWorkbook()
    if wb is not None:
        return getActiveWorkbook().activeSheet
    else:
        return None


def setActiveSheet(indexOrName: Union[str, int]):
    wb:Optional[Workbook] = getActiveWorkbook()
    if wb is None:
        raise ErrorReports.toException(
            ErrorReport(
                header=AppErrors.WorkbookNotExist.header,
                data=AppErrors.WorkbookNotExist.Data(indexOrName)
            )
        )
    wb.setActiveSheet(indexOrName)


def getSheet(nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
    wb = getActiveWorkbook()
    if wb is None:
        return None
    return wb.getSheet(nameOrIndex)


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
