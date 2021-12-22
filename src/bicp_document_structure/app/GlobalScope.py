"""
Global scope hold:
- app instances
- all the functions that user can use directly to query the active objects: see UserFunction.py for detail
"""

def getGlobals():
    return globals()