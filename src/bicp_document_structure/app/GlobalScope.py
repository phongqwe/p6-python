"""
Global scope should hold:
Important note: the content of global scope is decided by the init script run by clients.
- app instances
- all the functions that user can use directly to work with document objects:
    + UserFunctions.py
    + WorksheetFunctions.py
"""


def getGlobals():
    """this is the top-level globals() """
    if "_ipython_global_" in getP6Globals():
        return getP6Globals()["_ipython_global_"]
    else:
        return None

def getP6Globals():
    """this is the global of p6, to GlobalScope module"""
    return globals()

def setIPythonGlobals(ipythonGlobal):
    getP6Globals()["_ipython_global_"] = ipythonGlobal
