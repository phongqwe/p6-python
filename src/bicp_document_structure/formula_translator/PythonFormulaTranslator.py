from functools import partial

from antlr4 import *

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.ScriptFormulaTranslator import ScriptFormulaTranslator
from bicp_document_structure.formula_translator.antlr4.FormulaLexer import FormulaLexer
from bicp_document_structure.formula_translator.antlr4.FormulaParser import FormulaParser
from bicp_document_structure.formula_translator.errors.TranslatorErrors import TranslatorErrors
from bicp_document_structure.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class PythonFormulaTranslator(FormulaTranslator):
    scriptTranslator = ScriptFormulaTranslator()

    def __init__(self):
        self.parserError = None
        self.lexerError = None

    def translate(self, formula: str) -> Result:
        scriptRs = PythonFormulaTranslator.scriptTranslator.translate(formula)
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
            parser.addErrorListener(partial(self.onParserError, formula))
            tree = parser.formula()
            if self.parserError is not None or self.lexerError is not None:
                rt= Err(
                    ErrorReport(
                        TranslatorErrors.TranslatingErrHeader,
                        TranslatorErrors.TranslatingErrorData(self.lexerError, self.parserError),
                        loc="PythonFormulaTranslator.translate"
                    )
                )
                return rt
            else:
                visitor = PythonFormulaVisitor()
                out = visitor.visit(tree)
                return Ok(out)

    def onLexerError(self, formula, recognizer, offendingSymbol, line, column, msg, e):
        self.lexerError = TranslatorErrors.LexerErrorData(formula, recognizer, offendingSymbol, line, column, msg, e)

    def onParserError(self, formula, recognizer, offendingSymbol, line, column, msg, e):
        self.parserError = TranslatorErrors.ParserErrorData(formula, recognizer, offendingSymbol, line, column, msg, e)


class MyLexerErrorListener(DiagnosticErrorListener):
    def __init__(self, onError):
        super().__init__()
        self.onError = onError

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.onError(recognizer, offendingSymbol, line, column, msg, e)


class MyParserErrorListener(DiagnosticErrorListener):
    def __init__(self, onError):
        super().__init__()
        self.onError = onError

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.onError(recognizer, offendingSymbol, line, column, msg, e)
