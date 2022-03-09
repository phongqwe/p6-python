from typing import List, Optional, Any


def typeCheck(target, targetName: str, expectedType):
    """
    check if a target variable belong to a type
    :param target : target variable
    :param expectedType : type to check against
    :raise ValueError if target is not an instance of expectedType
    """
    if isinstance(target, expectedType):
        return
    else:
        raise ValueError(targetName + " is {act}. It must be {rt}".format(act=type(target), rt=str(expectedType)))


def multiTypeCheck(target, targetName: str, expectedTypeList: List):
    """
    check if a target variable belong to at least one type in a list of type
    :param target : target variable
    :param expectedTypeList : list of type to check against
    :raise ValueError if target is not an instance of at least one type in expectedTypeList
    """
    for type in expectedTypeList:
        if isinstance(target, type):
            return

    typeListStr = ", ".join(list(map(lambda t: str(t), expectedTypeList)))
    raise ValueError("{tn} must be one of these type {typeList}".format(tn=targetName, typeList=typeListStr))

def default(something:Optional[Any],defaultValue:Any):
    if something is None:
        return defaultValue
    else:
        return something
def makeGetter(result):
    def getter():
        return result
    return getter
