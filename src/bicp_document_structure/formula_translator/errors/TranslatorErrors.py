from typing import Optional

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader


class TranslatorErrors:
    prefix = "Translator Error "
    TranslatingErrHeader = ErrorHeader("{pf}0".format(pf=prefix),"translating error")
    LexerErrorHeader = ErrorHeader("{pf}1".format(pf=prefix),"lexer error")
    ParserErrorHeader = ErrorHeader("{pf}3".format(pf=prefix),"parser error")
    NotAScriptCallHeader = ErrorHeader("{pf}2".format(pf=prefix),"input is not a =SCRIPT() call")

    class NotAScriptCallData:
        def __init__(self,formula):
            self.formula = formula

    class LexerErrorData:
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

    class ParserErrorData:
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

    class TranslatingErrorData:
        def __init__(self, lexerErr,parserErr):
            self.lexerErr = lexerErr
            self.parserErr = parserErr

