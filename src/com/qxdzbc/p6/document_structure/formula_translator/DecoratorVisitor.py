from abc import ABC

from com.qxdzbc.p6.document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from com.qxdzbc.p6.document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor


class DecoratorVisitor(FormulaVisitor, ABC):

    def __init__(self, visitor: FormulaVisitor):
        self._visitor = visitor

    def visitZFormula(self, ctx: FormulaParser.ZFormulaContext):
        return self._visitor.visitZFormula(ctx)

    def visitAddSubExpr(self, ctx: FormulaParser.AddSubExprContext):
        return self._visitor.visitAddSubExpr(ctx)

    def visitUnExpr(self, ctx: FormulaParser.UnExprContext):
        return self._visitor.visitUnExpr(ctx)

    def visitMulDivModExpr(self, ctx: FormulaParser.MulDivModExprContext):
        return self._visitor.visitMulDivModExpr(ctx)

    def visitSheetRangeAddrExpr(self, ctx: FormulaParser.SheetRangeAddrExprContext):
        return self._visitor.visitSheetRangeAddrExpr(ctx)

    def visitPowExpr(self, ctx: FormulaParser.PowExprContext):
        return self._visitor.visitPowExpr(ctx)

    def visitFunCall(self, ctx: FormulaParser.FunCallContext):
        return self._visitor.visitFunCall(ctx)

    def visitParenExpr(self, ctx: FormulaParser.ParenExprContext):
        return self._visitor.visitParenExpr(ctx)

    def visitLiteral(self, ctx: FormulaParser.LiteralContext):
        return self._visitor.visitLiteral(ctx)

    def visitFunctionCall(self, ctx: FormulaParser.FunctionCallContext):
        return self._visitor.visitFunctionCall(ctx)

    def visitFunctionName(self, ctx: FormulaParser.FunctionNameContext):
        return self._visitor.visitFunctionName(ctx)

    def visitPairCellAddress(self, ctx: FormulaParser.PairCellAddressContext):
        return self._visitor.visitPairCellAddress(ctx)

    def visitOneCellAddress(self, ctx: FormulaParser.OneCellAddressContext):
        return self._visitor.visitOneCellAddress(ctx)

    def visitColAddress(self, ctx: FormulaParser.ColAddressContext):
        return self._visitor.visitColAddress(ctx)

    def visitRowAddress(self, ctx: FormulaParser.RowAddressContext):
        return self._visitor.visitRowAddress(ctx)

    def visitParensAddress(self, ctx: FormulaParser.ParensAddressContext):
        return self._visitor.visitParensAddress(ctx)

    def visitCellAddress(self, ctx: FormulaParser.CellAddressContext):
        return self._visitor.visitCellAddress(ctx)

    def visitLit(self, ctx: FormulaParser.LitContext):
        return self._visitor.visitLit(ctx)
