def convertExceptionToStr(exception:Exception)->str:
    if isinstance(exception,RecursionError):
        return "ERR:Circular Ref"
    else:
        return "ERR:" + str(exception)


class CellUtils:
    @staticmethod
    def parseValue(value:str):
        """attempt to parse the string to int, float, then str"""
        try:
            asInt=int(value)
            return asInt
        except Exception:
            try:
                asFloat = float(value)
                return asFloat
            except Exception:
                return value


