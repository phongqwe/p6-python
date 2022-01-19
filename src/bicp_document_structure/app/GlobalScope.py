"""
Global scope hold:
- app instances
- all the functions that user can use directly to query the active objects: see UserFunction.py for detail
"""

def getGlobals():
    return getP6Globals()["_ipython_global_"]

def getP6Globals():
    return globals()

def setIPythonGlobals(ipythonGlobal):
    getP6Globals()["_ipython_global_"] = ipythonGlobal