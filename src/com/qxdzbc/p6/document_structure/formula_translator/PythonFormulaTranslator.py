from functools import partial

from antlr4 import *

from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.ScriptFormulaTranslator import ScriptFormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.antlr4.FormulaLexer import FormulaLexer
from com.qxdzbc.p6.document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from com.qxdzbc.p6.document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor
from com.qxdzbc.p6.document_structure.formula_translator.errors.MyLexerErrorListener import MyLexerErrorListener
from com.qxdzbc.p6.document_structure.formula_translator.errors.MyParserErrorListener import MyParserErrorListener
from com.qxdzbc.p6.document_structure.formula_translator.errors.TranslatorErrors import TranslatorErrors
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result


class PythonFormulaTranslator(FormulaTranslator):

    """
    A neutral translator. Its behavior can be altered by using different FormulaVisitor
    """
    scriptTranslator = ScriptFormulaTranslator()

    def __init__(self, visitor: FormulaVisitor):
        self.parserError = None
        self.lexerError = None
        self.__visitor:FormulaVisitor = visitor

    def translate(self, formula: str) -> Result[str, ErrorReport]:
        scriptRs: Result[str, ErrorReport] = PythonFormulaTranslator.scriptTranslator.translate(formula)
        if scriptRs.isOk():
            return scriptRs
        else:
            self.parserError = None
            self.lexerError = None
            charStream = InputStream(formula)
            lexer = FormulaLexer(charStream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(MyLexerErrorListener(partial(self.onLexerError, formula)))
            tokenStream = CommonTokenStream(lexer)
            parser = FormulaParser(tokenStream)
            parser.removeErrorListeners()
            errorListener = MyParserErrorListener(partial(self.onParserError, formula))
            parser.addErrorListener(errorListener)
            tree = parser.formula()
            if self.parserError is not None or self.lexerError is not None:
                rt = Err(
                    ErrorReport(
                        TranslatorErrors.TranslatingErr.header,
                        TranslatorErrors.TranslatingErr.Data(self.lexerError, self.parserError),
                    )
                )
                return rt
            else:
                out = self.__visitor.visit(tree)
                return Ok(out)

    def onLexerError(self, formula, recognizer, offendingSymbol, line, column, msg, e):
        self.lexerError = TranslatorErrors.LexerError.Data(formula, recognizer, offendingSymbol, line, column, msg, e)

    def onParserError(self, formula, recognizer, offendingSymbol, line, column, msg, e):
        self.parserError = TranslatorErrors.ParserError.Data(formula, recognizer, offendingSymbol, line, column, msg, e)
