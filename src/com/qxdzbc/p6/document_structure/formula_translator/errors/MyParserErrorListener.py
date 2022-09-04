from antlr4 import DiagnosticErrorListener


class MyParserErrorListener(DiagnosticErrorListener):
    def __init__(self, onError):
        super().__init__()
        self.onError = onError

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.onError(recognizer, offendingSymbol, line, column, msg, e)
