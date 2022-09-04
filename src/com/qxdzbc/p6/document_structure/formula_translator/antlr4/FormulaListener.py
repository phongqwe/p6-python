# Generated from Formula.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FormulaParser import FormulaParser
else:
    from FormulaParser import FormulaParser

# This class defines a complete listener for a parse tree produced by FormulaParser.
class FormulaListener(ParseTreeListener):

    # Enter a parse tree produced by FormulaParser#zFormula.
    def enterZFormula(self, ctx:FormulaParser.ZFormulaContext):
        pass

    # Exit a parse tree produced by FormulaParser#zFormula.
    def exitZFormula(self, ctx:FormulaParser.ZFormulaContext):
        pass


    # Enter a parse tree produced by FormulaParser#addSubExpr.
    def enterAddSubExpr(self, ctx:FormulaParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#addSubExpr.
    def exitAddSubExpr(self, ctx:FormulaParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#unExpr.
    def enterUnExpr(self, ctx:FormulaParser.UnExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#unExpr.
    def exitUnExpr(self, ctx:FormulaParser.UnExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#mulDivModExpr.
    def enterMulDivModExpr(self, ctx:FormulaParser.MulDivModExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#mulDivModExpr.
    def exitMulDivModExpr(self, ctx:FormulaParser.MulDivModExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#sheetRangeAddrExpr.
    def enterSheetRangeAddrExpr(self, ctx:FormulaParser.SheetRangeAddrExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#sheetRangeAddrExpr.
    def exitSheetRangeAddrExpr(self, ctx:FormulaParser.SheetRangeAddrExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#powExpr.
    def enterPowExpr(self, ctx:FormulaParser.PowExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#powExpr.
    def exitPowExpr(self, ctx:FormulaParser.PowExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#funCall.
    def enterFunCall(self, ctx:FormulaParser.FunCallContext):
        pass

    # Exit a parse tree produced by FormulaParser#funCall.
    def exitFunCall(self, ctx:FormulaParser.FunCallContext):
        pass


    # Enter a parse tree produced by FormulaParser#parenExpr.
    def enterParenExpr(self, ctx:FormulaParser.ParenExprContext):
        pass

    # Exit a parse tree produced by FormulaParser#parenExpr.
    def exitParenExpr(self, ctx:FormulaParser.ParenExprContext):
        pass


    # Enter a parse tree produced by FormulaParser#literal.
    def enterLiteral(self, ctx:FormulaParser.LiteralContext):
        pass

    # Exit a parse tree produced by FormulaParser#literal.
    def exitLiteral(self, ctx:FormulaParser.LiteralContext):
        pass


    # Enter a parse tree produced by FormulaParser#functionCall.
    def enterFunctionCall(self, ctx:FormulaParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by FormulaParser#functionCall.
    def exitFunctionCall(self, ctx:FormulaParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by FormulaParser#functionName.
    def enterFunctionName(self, ctx:FormulaParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by FormulaParser#functionName.
    def exitFunctionName(self, ctx:FormulaParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by FormulaParser#pairCellAddress.
    def enterPairCellAddress(self, ctx:FormulaParser.PairCellAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#pairCellAddress.
    def exitPairCellAddress(self, ctx:FormulaParser.PairCellAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#oneCellAddress.
    def enterOneCellAddress(self, ctx:FormulaParser.OneCellAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#oneCellAddress.
    def exitOneCellAddress(self, ctx:FormulaParser.OneCellAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#colAddress.
    def enterColAddress(self, ctx:FormulaParser.ColAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#colAddress.
    def exitColAddress(self, ctx:FormulaParser.ColAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#rowAddress.
    def enterRowAddress(self, ctx:FormulaParser.RowAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#rowAddress.
    def exitRowAddress(self, ctx:FormulaParser.RowAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#parensAddress.
    def enterParensAddress(self, ctx:FormulaParser.ParensAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#parensAddress.
    def exitParensAddress(self, ctx:FormulaParser.ParensAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#cellAddress.
    def enterCellAddress(self, ctx:FormulaParser.CellAddressContext):
        pass

    # Exit a parse tree produced by FormulaParser#cellAddress.
    def exitCellAddress(self, ctx:FormulaParser.CellAddressContext):
        pass


    # Enter a parse tree produced by FormulaParser#lit.
    def enterLit(self, ctx:FormulaParser.LitContext):
        pass

    # Exit a parse tree produced by FormulaParser#lit.
    def exitLit(self, ctx:FormulaParser.LitContext):
        pass



del FormulaParser