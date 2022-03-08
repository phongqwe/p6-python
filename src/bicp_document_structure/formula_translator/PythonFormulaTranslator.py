from functools import partial

from antlr4 import *

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.ScriptFormulaTranslator import ScriptFormulaTranslator
from bicp_document_structure.formula_translator.antlr4.FormulaLexer import FormulaLexer
from bicp_document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from bicp_document_structure.formula_translator.antlr4.FormulaVisitor import FormulaVisitor
from bicp_document_structure.formula_translator.errors.MyLexerErrorListener import MyLexerErrorListener
from bicp_document_structure.formula_translator.errors.MyParserErrorListener import MyParserErrorListener
from bicp_document_structure.formula_translator.errors.TranslatorErrors import TranslatorErrors
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class PythonFormulaTranslator(FormulaTranslator):
    scriptTranslator = ScriptFormulaTranslator()

    def __init__(self, visitor: FormulaVisitor|None = None):
        self.parserError = None
        self.lexerError = None
        if visitor is None:
            visitor = PythonFormulaVisitor()
        self.__visitor = visitor

    def translate(self, formula: str) -> Result[str,ErrorReport]:
        scriptRs:Result[str,ErrorReport] = PythonFormulaTranslator.scriptTranslator.translate(formula)
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
                        loc = "PythonFormulaTranslator.translate"
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




