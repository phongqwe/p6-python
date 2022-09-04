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
        raise ValueError(targetName + " is {act}. It must be {rt}".format(act = type(target), rt = str(expectedType)))


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
    raise ValueError("{tn} must be one of these type {typeList}".format(tn = targetName, typeList = typeListStr))


def default(something: Optional[Any], defaultValue: Any):
    if something is None:
        return defaultValue
    else:
        return something


def makeGetter(result):
    """create a getter function that returns the input obj"""
    def getter():
        return result

    return getter

def compareList(l1:list,l2:list)->bool:
    sameLen = len(l1) == len(l2)
    l1ContainL2 = all(elem in l1 for elem in l2)
    l2ContainL1 = all(elem in l2 for elem in l1)
    return sameLen and l1ContainL2 and l2ContainL1

def replaceKey(mp:dict, oldKey:Any, newKey:Any)->dict:
    newMap = {}
    for (k,v) in mp.items():
        key = k
        if k == oldKey:
            key = newKey
        newMap[key] = v
    return newMap



