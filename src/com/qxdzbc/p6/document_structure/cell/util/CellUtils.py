def convertExceptionToStr(exception: Exception) -> str:
    if isinstance(exception, RecursionError):
        return "ERR:Circular Ref"
    else:
        return "ERR:" + str(exception)


class CellUtils:
    @staticmethod
    def parseValue(value: str) -> int | float | str | bool:
        """attempt to parse a string to int, float, bool, then str"""
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

    @staticmethod
    def isNumericString(value:str):
        """
        "\'123" => true
        "\'abc" => false
        :param value:
        :return:
        """
        if isinstance(value,str):
            if value.startswith("\'"):
                theRest = value[1:]
                try:
                    num = float(theRest)
                    return True
                except Exception as e:
                    return False
        else:
            return False
    @staticmethod
    def isFormula(text:str)->bool:
        return text.strip().startswith("=")