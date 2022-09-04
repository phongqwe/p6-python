from typing import Optional

from com.qxdzbc.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader

__errPrefix = "Translator Error "
def _errPrefix():
    return __errPrefix

class TranslatorErrors:
    prefix = "Translator Error "

    class TranslatingErr:
        header = ErrorHeader(f"{_errPrefix()}0","translating error")
        class Data:
            def __init__(self, lexerErr, parserErr):
                self.lexerErr = lexerErr
                self.parserErr = parserErr

    class LexerError:
        header = ErrorHeader(f"{_errPrefix()}1","lexer error")
        class Data:
            def __init__(self, formula: str, recognizer, offendingSymbol,
                         line: int, charPositionInLine: int,
                         msg: Optional[str], recognitionException):
                self.formula = formula
                self.recognizer = recognizer
                self.offendingSymbol = offendingSymbol
                self.line = line
                self.charPositionInLine = charPositionInLine
                self.msg = msg
                self.recognitionException = recognitionException

    class ParserError:
        header = ErrorHeader(f"{_errPrefix()}3","parser error")

        class Data:
            def __init__(self, formula: str, recognizer, offendingSymbol,
                         line: int, charPositionInLine: int,
                         msg: Optional[str], recognitionException):
                self.formula = formula
                self.recognizer = recognizer
                self.offendingSymbol = offendingSymbol
                self.line = line
                self.charPositionInLine = charPositionInLine
                self.msg = msg
                self.recognitionException = recognitionException
    class NotAScriptCallError:
        header = ErrorHeader(f"{_errPrefix()}2", "input is not a =SCRIPT() call")

        class Data:
            def __init__(self, formula):
                self.formula = formula