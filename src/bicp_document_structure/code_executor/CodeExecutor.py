import ast


class CodeExecutor:
    @staticmethod
    def evalCode(code: str, globalScope, localScope):
        """ Execute a piece of code, then return the result of the last line"""
        # parse the code into an Abstract syntax tree
        codeAst = ast.parse(code)
        # extract the last expression
        lastNode = codeAst.body.pop()
        lastExp = ast.Expression(lastNode.value)
        # compile and execute the code, not including the last expr
        exec(compile(codeAst, '<string>', mode='exec'), globalScope, localScope)
        # evaluate the last expr
        lastEvalRs = eval(compile(lastExp, '<string>', mode='eval'), globalScope, localScope)
        return lastEvalRs
