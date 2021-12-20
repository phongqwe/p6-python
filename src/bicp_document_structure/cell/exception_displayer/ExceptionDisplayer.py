def convertExceptionToStr(exception:Exception)->str:
    if isinstance(exception,RecursionError):
        return "ERR:Circular Ref"
    else:
        return "ERR:" + str(exception)
