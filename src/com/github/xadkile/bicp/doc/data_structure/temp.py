import ast


def evalCode(code: str, globalDict, localDict):
    # parse the code into an Abstract syntax tree
    codeAst = ast.parse(code)

    # extract the last expression
    lastNode = codeAst.body.pop()
    lastExp = ast.Expression(lastNode.value)

    # compile and execute the code, not including the last expr
    exec(compile(codeAst, '<string>', mode='exec'), globalDict, localDict)

    # evaluate the last expr
    lastEvalRs = eval(compile(lastExp, '<string>', mode='eval'), globalDict, localDict)

    globals().update(globalDict)

    return lastEvalRs
