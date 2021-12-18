def typeCheck(target, targetName: str, expectedType):
    if isinstance(target, expectedType):
        return
    else:
        raise ValueError(targetName + " is {act}. It must be {rt}".format(act=type(target), rt=str(expectedType)))
