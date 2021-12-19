from typing import Optional

from bicp_document_structure.app.App import App
from bicp_document_structure.app.SingleBookApp import SingleBookApp
# class AppInit:
#     __appInstance = None
#     __globals = None
#
#     @staticmethod
#     def startApp():
#         AppInit.getApp()
#         AppInit.globals()
#
#     @staticmethod
#     def getApp() -> App:
#         if AppInit.__appInstance is None:
#             AppInit.__appInstance = SingleBookApp()
#         return AppInit.__appInstance
#     # @staticmethod
#     # def getActiveWorkbook(self)->:
#
#
#     @staticmethod
#     def globals():
#         if AppInit.__globals is None:
#             g = {"app": AppInit.getApp(), }
#             gs = globals().copy()
#             gs.update(g)
#             # gs["globalsX"] = gs
#             AppInit.__globals = gs
#         return AppInit.__globals
from bicp_document_structure.sheet.Worksheet import Worksheet
from bicp_document_structure.workbook.WorkBook import Workbook

__appInstance = None
__globals = None

def startApp():
    getApp()
    getGlobals()

def getApp() -> App:
    global __appInstance
    if __appInstance is None:
        __appInstance = SingleBookApp()
    return __appInstance

def getGlobals():
    global __globals
    if __globals is None:
        g = {"app": getApp(), }
        gs = globals().copy()
        gs.update(g)
        # gs["globalsX"] = gs
        __globals = gs
    return __globals

"""
what I want:
i want a some function so that I can quickly access:
    - the current workbook: activeWorkbook.
    - the current worksheet of the current workbook: activeSheet()
    - quickly access range from the active sheet like in excel: activeSheet.range(), or range()
"""


def activeWorkbook()->Optional[Workbook]:
    """for this to work, I need to maintain an object that watch for workbook-change events"""
    pass

def activeSheet()->Optional[Worksheet]:
    """active sheet of the activeWorkbook"""
    activeWb = activeWorkbook()
    if activeWb is not None:
        return activeWb.activeSheet
    else:
        return None
