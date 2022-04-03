from typing import Union

from com.emeraldblast.p6.document_structure.formula_translator.PythonLangElements import PythonLangElements
from com.emeraldblast.p6.document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from com.emeraldblast.p6.document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor
from com.emeraldblast.p6.document_structure.formula_translator.mapper.PythonMapper import PythonMapper


class PythonFormulaVisitor(FormulaVisitor):

    def __init__(self):
        self.mapper = PythonMapper.instance()

    def visitZFormula(self, ctx: FormulaParser.ZFormulaContext):
        if ctx is not None and ctx.expr() is not None:
            return self.visit(ctx.expr())
        else:
            return ""

    def visitAddSubExpr(self, ctx: FormulaParser.AddSubExprContext):
        expr0 = self.visit(ctx.expr(0))
        op = ctx.op.text
        expr1 = self.visit(ctx.expr(1))
        return "{expr0}{op}{expr1}".format(
            expr0=expr0, op=op, expr1=expr1
        )

    def visitUnExpr(self, ctx: FormulaParser.UnExprContext):
        if ctx is not None:
            expr = self.visit(ctx.expr())
            op = ctx.op.text
            return "{}{}".format(op, expr)
        else:
            return ""

    def visitMulDivModExpr(self, ctx: FormulaParser.MulDivModExprContext):
        expr0 = self.visit(ctx.expr(0))
        op = ctx.op.text
        expr1 = self.visit(ctx.expr(1))
        return "{expr0}{op}{expr1}".format(
            expr0=expr0, op=op, expr1=expr1
        )

    def visitSheetRangeAddrExpr(self, ctx: FormulaParser.SheetRangeAddrExprContext):
        if ctx.SHEET_PREFIX() is not None:
            rawSheetName = ctx.SHEET_PREFIX().getText()
        else:
            rawSheetName = None
        sheetName: str = self._extractSheetName(rawSheetName)
        getSheet: str = ""
        if len(sheetName) != 0:
            getSheet = self.mapper.getWorksheet(sheetName) + "."
        rangeObj = self.visit(ctx.rangeAddress())
        return "{getSheet}{rangeObj}".format(
            getSheet=getSheet,
            rangeObj=rangeObj
        )

    def visitPowExpr(self, ctx: FormulaParser.PowExprContext):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        return "{}**{}".format(expr0, expr1)

    def visitFunCall(self, ctx: FormulaParser.FunCallContext):
        if ctx is not None and ctx.functionCall() is not None and ctx.functionCall().expr() is not None:
            functionName = self.visit(ctx.functionCall().functionName())
            name = "{functionLib}.{functionName}".format(
                functionLib=PythonLangElements.worksheetFunctions,
                functionName=functionName
            )
            args = list(map(lambda c: self.visit(c), ctx.functionCall().expr()))
            return "{name}({args})".format(
                name=name,
                args=",".join(args)
            )
        else:
            return ""

    def visitParenExpr(self, ctx: FormulaParser.ParenExprContext):
        if ctx is not None:
            return "({})".format(
                self.visit(ctx.expr())
            )
        else:
            return ""

    def visitLiteral(self, ctx: FormulaParser.LiteralContext):
        if ctx is not None:
            return ctx.getText()
        else:
            return ""

    def visitFunctionCall(self, ctx: FormulaParser.FunctionCallContext):
        functionName = self.visit(ctx.functionName())
        argsExpr = ctx.expr()
        if argsExpr is not None:
            args = ", ".join(list(map(lambda c: self.visit(c), argsExpr)))
        else:
            args = []
        return "{functionLib}.{fname}({args})".format(
            functionLib=PythonLangElements.worksheetFunctions,
            fname=functionName,
            args=args
        )

    def visitFunctionName(self, ctx: FormulaParser.FunctionNameContext):
        return ctx.getText()

    def visitPairCellAddress(self, ctx: FormulaParser.PairCellAddressContext):
        cell0 = ctx.cellAddress(0).getText()
        cell1 = ctx.cellAddress(1).getText()
        rangeAddress = self.mapper.formatRangeAddress("{c0}:{c1}".format(c0=cell0, c1=cell1))
        return self.mapper.getRange(rangeAddress)

    def visitOneCellAddress(self, ctx: FormulaParser.OneCellAddressContext):
        return self.mapper.getCell(self.mapper.formatRangeAddress(ctx.cellAddress().getText())) + ".value"

    def visitColAddress(self, ctx: FormulaParser.ColAddressContext):
        return self.mapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))

    def visitRowAddress(self, ctx: FormulaParser.RowAddressContext):
        return self.mapper.getRange(self.mapper.formatRangeAddress(ctx.getText()))

    def visitParensAddress(self, ctx: FormulaParser.ParensAddressContext):
        return "({c})".format(
            c=self.visit(ctx.rangeAddress())
        )

    def visitCellAddress(self, ctx: FormulaParser.CellAddressContext):
        return super().visitCellAddress(ctx)

    def visitLit(self, ctx: FormulaParser.LitContext):
        return ctx.getText()

    def _extractSheetName(self, rawSheetName: Union[str, None]) -> str:
        """
        extract sheet name from something like this: 'sheet1 qbc'!
        remove the trailing "!", and the single quote
        :param rawSheetName:
        :return:
        """
        if rawSheetName is None or len(rawSheetName) == 0:
            return ""
        sName = rawSheetName
        if sName.endswith("!"):
            sName = sName[0:len(rawSheetName)-1]
        if sName.startswith("\'"):
            sName= sName[1: len(sName)]
        if sName.endswith("\'"):
            sName = sName[0: len(sName)-1]
        return sName
