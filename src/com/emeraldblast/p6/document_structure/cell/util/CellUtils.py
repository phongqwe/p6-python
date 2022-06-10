def convertExceptionToStr(exception: Exception) -> str:
    if isinstance(exception, RecursionError):
        return "ERR:Circular Ref"
    else:
        return "ERR:" + str(exception)


class CellUtils:
    @staticmethod
    def parseValue(value: str) -> int | float | str | bool:
        """attempt to parse the string to int, float, bool, then str"""
        try:
            asInt = int(value)
            return asInt
        except Exception:
            try:
                asFloat = float(value)
                return asFloat
            except Exception:
                if value == "True":
                    return True
                if value == "False":
                    return False
                return value
