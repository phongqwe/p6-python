# Generated from Formula.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FormulaParser import FormulaParser
else:
    from FormulaParser import FormulaParser

# This class defines a complete generic visitor for a parse tree produced by FormulaParser.

class FormulaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FormulaParser#zFormula.
    def visitZFormula(self, ctx:FormulaParser.ZFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#addSubExpr.
    def visitAddSubExpr(self, ctx:FormulaParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#unExpr.
    def visitUnExpr(self, ctx:FormulaParser.UnExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#mulDivModExpr.
    def visitMulDivModExpr(self, ctx:FormulaParser.MulDivModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#sheetRangeAddrExpr.
    def visitSheetRangeAddrExpr(self, ctx:FormulaParser.SheetRangeAddrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#powExpr.
    def visitPowExpr(self, ctx:FormulaParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#funCall.
    def visitFunCall(self, ctx:FormulaParser.FunCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#parenExpr.
    def visitParenExpr(self, ctx:FormulaParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#literal.
    def visitLiteral(self, ctx:FormulaParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#functionCall.
    def visitFunctionCall(self, ctx:FormulaParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#functionName.
    def visitFunctionName(self, ctx:FormulaParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#pairCellAddress.
    def visitPairCellAddress(self, ctx:FormulaParser.PairCellAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#oneCellAddress.
    def visitOneCellAddress(self, ctx:FormulaParser.OneCellAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#colAddress.
    def visitColAddress(self, ctx:FormulaParser.ColAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#rowAddress.
    def visitRowAddress(self, ctx:FormulaParser.RowAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#parensAddress.
    def visitParensAddress(self, ctx:FormulaParser.ParensAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#cellAddress.
    def visitCellAddress(self, ctx:FormulaParser.CellAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormulaParser#lit.
    def visitLit(self, ctx:FormulaParser.LitContext):
        return self.visitChildren(ctx)



del FormulaParser