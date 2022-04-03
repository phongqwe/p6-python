# Generated from Formula.g4 by ANTLR 4.9.2
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *

if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\24")
        buf.write("`\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\5\3\37\n\3\3\3\5\3\"\n\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\7\3-\n\3\f\3\16\3\60\13\3\3\4\3\4\3\4\5")
        buf.write("\4\65\n\4\3\4\3\4\7\49\n\4\f\4\16\4<\13\4\3\4\5\4?\n\4")
        buf.write("\3\4\3\4\3\5\3\5\7\5E\n\5\f\5\16\5H\13\5\3\6\3\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6Y\n")
        buf.write("\6\3\7\3\7\3\7\3\b\3\b\3\b\2\3\4\t\2\4\6\b\n\f\16\2\6")
        buf.write("\3\2\17\20\4\2\r\16\21\21\4\2\t\t\13\13\3\2\n\f\2h\2\20")
        buf.write("\3\2\2\2\4!\3\2\2\2\6\61\3\2\2\2\bB\3\2\2\2\nX\3\2\2\2")
        buf.write("\fZ\3\2\2\2\16]\3\2\2\2\20\21\7\3\2\2\21\22\5\4\3\2\22")
        buf.write("\23\7\2\2\3\23\3\3\2\2\2\24\25\b\3\1\2\25\"\5\6\4\2\26")
        buf.write("\27\7\4\2\2\27\30\5\4\3\2\30\31\7\5\2\2\31\"\3\2\2\2\32")
        buf.write("\"\5\16\b\2\33\34\t\2\2\2\34\"\5\4\3\7\35\37\7\b\2\2\36")
        buf.write("\35\3\2\2\2\36\37\3\2\2\2\37 \3\2\2\2 \"\5\n\6\2!\24\3")
        buf.write("\2\2\2!\26\3\2\2\2!\32\3\2\2\2!\33\3\2\2\2!\36\3\2\2\2")
        buf.write("\".\3\2\2\2#$\f\6\2\2$%\7\22\2\2%-\5\4\3\7&\'\f\5\2\2")
        buf.write("\'(\t\3\2\2(-\5\4\3\6)*\f\4\2\2*+\t\2\2\2+-\5\4\3\5,#")
        buf.write("\3\2\2\2,&\3\2\2\2,)\3\2\2\2-\60\3\2\2\2.,\3\2\2\2./\3")
        buf.write("\2\2\2/\5\3\2\2\2\60.\3\2\2\2\61\62\5\b\5\2\62\64\7\4")
        buf.write("\2\2\63\65\5\4\3\2\64\63\3\2\2\2\64\65\3\2\2\2\65:\3\2")
        buf.write("\2\2\66\67\7\6\2\2\679\5\4\3\28\66\3\2\2\29<\3\2\2\2:")
        buf.write("8\3\2\2\2:;\3\2\2\2;>\3\2\2\2<:\3\2\2\2=?\7\6\2\2>=\3")
        buf.write("\2\2\2>?\3\2\2\2?@\3\2\2\2@A\7\5\2\2A\7\3\2\2\2BF\7\t")
        buf.write("\2\2CE\t\4\2\2DC\3\2\2\2EH\3\2\2\2FD\3\2\2\2FG\3\2\2\2")
        buf.write("G\t\3\2\2\2HF\3\2\2\2IJ\5\f\7\2JK\7\7\2\2KL\5\f\7\2LY")
        buf.write("\3\2\2\2MY\5\f\7\2NO\7\t\2\2OP\7\7\2\2PY\7\t\2\2QR\7\13")
        buf.write("\2\2RS\7\7\2\2SY\7\13\2\2TU\7\4\2\2UV\5\n\6\2VW\7\5\2")
        buf.write("\2WY\3\2\2\2XI\3\2\2\2XM\3\2\2\2XN\3\2\2\2XQ\3\2\2\2X")
        buf.write("T\3\2\2\2Y\13\3\2\2\2Z[\7\t\2\2[\\\7\13\2\2\\\r\3\2\2")
        buf.write("\2]^\t\5\2\2^\17\3\2\2\2\13\36!,.\64:>FX")
        return buf.getvalue()


class FormulaParser ( Parser ):

    grammarFileName = "Formula.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'('", "')'", "','", "':'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'*'", "'/'", "'+'", "'-'", "'%'", "'^'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "SHEET_PREFIX", "ID", "FLOAT_NUMBER", 
                      "INT", "STRING", "MUL", "DIV", "ADD", "SUB", "MOD", 
                      "EXP", "NEWLINE", "WS" ]

    RULE_formula = 0
    RULE_expr = 1
    RULE_functionCall = 2
    RULE_functionName = 3
    RULE_rangeAddress = 4
    RULE_cellAddress = 5
    RULE_lit = 6

    ruleNames =  [ "formula", "expr", "functionCall", "functionName", "rangeAddress", 
                   "cellAddress", "lit" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    SHEET_PREFIX=6
    ID=7
    FLOAT_NUMBER=8
    INT=9
    STRING=10
    MUL=11
    DIV=12
    ADD=13
    SUB=14
    MOD=15
    EXP=16
    NEWLINE=17
    WS=18

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FormulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FormulaParser.RULE_formula

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ZFormulaContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(FormulaParser.ExprContext,0)

        def EOF(self):
            return self.getToken(FormulaParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterZFormula" ):
                listener.enterZFormula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitZFormula" ):
                listener.exitZFormula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitZFormula" ):
                return visitor.visitZFormula(self)
            else:
                return visitor.visitChildren(self)



    def formula(self):

        localctx = FormulaParser.FormulaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_formula)
        try:
            localctx = FormulaParser.ZFormulaContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.match(FormulaParser.T__0)
            self.state = 15
            self.expr(0)
            self.state = 16
            self.match(FormulaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FormulaParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AddSubExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FormulaParser.ExprContext)
            else:
                return self.getTypedRuleContext(FormulaParser.ExprContext,i)

        def ADD(self):
            return self.getToken(FormulaParser.ADD, 0)
        def SUB(self):
            return self.getToken(FormulaParser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSubExpr" ):
                listener.enterAddSubExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSubExpr" ):
                listener.exitAddSubExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSubExpr" ):
                return visitor.visitAddSubExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(FormulaParser.ExprContext,0)

        def SUB(self):
            return self.getToken(FormulaParser.SUB, 0)
        def ADD(self):
            return self.getToken(FormulaParser.ADD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnExpr" ):
                listener.enterUnExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnExpr" ):
                listener.exitUnExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnExpr" ):
                return visitor.visitUnExpr(self)
            else:
                return visitor.visitChildren(self)


    class MulDivModExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FormulaParser.ExprContext)
            else:
                return self.getTypedRuleContext(FormulaParser.ExprContext,i)

        def MUL(self):
            return self.getToken(FormulaParser.MUL, 0)
        def DIV(self):
            return self.getToken(FormulaParser.DIV, 0)
        def MOD(self):
            return self.getToken(FormulaParser.MOD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDivModExpr" ):
                listener.enterMulDivModExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDivModExpr" ):
                listener.exitMulDivModExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDivModExpr" ):
                return visitor.visitMulDivModExpr(self)
            else:
                return visitor.visitChildren(self)


    class SheetRangeAddrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def rangeAddress(self):
            return self.getTypedRuleContext(FormulaParser.RangeAddressContext,0)

        def SHEET_PREFIX(self):
            return self.getToken(FormulaParser.SHEET_PREFIX, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSheetRangeAddrExpr" ):
                listener.enterSheetRangeAddrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSheetRangeAddrExpr" ):
                listener.exitSheetRangeAddrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSheetRangeAddrExpr" ):
                return visitor.visitSheetRangeAddrExpr(self)
            else:
                return visitor.visitChildren(self)


    class PowExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FormulaParser.ExprContext)
            else:
                return self.getTypedRuleContext(FormulaParser.ExprContext,i)

        def EXP(self):
            return self.getToken(FormulaParser.EXP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowExpr" ):
                listener.enterPowExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowExpr" ):
                listener.exitPowExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowExpr" ):
                return visitor.visitPowExpr(self)
            else:
                return visitor.visitChildren(self)


    class FunCallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCall(self):
            return self.getTypedRuleContext(FormulaParser.FunctionCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunCall" ):
                listener.enterFunCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunCall" ):
                listener.exitFunCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunCall" ):
                return visitor.visitFunCall(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(FormulaParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class LiteralContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def lit(self):
            return self.getTypedRuleContext(FormulaParser.LitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = FormulaParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = FormulaParser.FunCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 19
                self.functionCall()
                pass

            elif la_ == 2:
                localctx = FormulaParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 20
                self.match(FormulaParser.T__1)
                self.state = 21
                self.expr(0)
                self.state = 22
                self.match(FormulaParser.T__2)
                pass

            elif la_ == 3:
                localctx = FormulaParser.LiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 24
                self.lit()
                pass

            elif la_ == 4:
                localctx = FormulaParser.UnExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 25
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==FormulaParser.ADD or _la==FormulaParser.SUB):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 26
                self.expr(5)
                pass

            elif la_ == 5:
                localctx = FormulaParser.SheetRangeAddrExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==FormulaParser.SHEET_PREFIX:
                    self.state = 27
                    self.match(FormulaParser.SHEET_PREFIX)


                self.state = 30
                self.rangeAddress()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 44
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 42
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = FormulaParser.PowExprContext(self, FormulaParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 33
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 34
                        localctx.op = self.match(FormulaParser.EXP)
                        self.state = 35
                        self.expr(5)
                        pass

                    elif la_ == 2:
                        localctx = FormulaParser.MulDivModExprContext(self, FormulaParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 36
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 37
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FormulaParser.MUL) | (1 << FormulaParser.DIV) | (1 << FormulaParser.MOD))) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 38
                        self.expr(4)
                        pass

                    elif la_ == 3:
                        localctx = FormulaParser.AddSubExprContext(self, FormulaParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 39
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 40
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==FormulaParser.ADD or _la==FormulaParser.SUB):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 41
                        self.expr(3)
                        pass

             
                self.state = 46
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionName(self):
            return self.getTypedRuleContext(FormulaParser.FunctionNameContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FormulaParser.ExprContext)
            else:
                return self.getTypedRuleContext(FormulaParser.ExprContext,i)


        def getRuleIndex(self):
            return FormulaParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = FormulaParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.functionName()
            self.state = 48
            self.match(FormulaParser.T__1)
            self.state = 50
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FormulaParser.T__1) | (1 << FormulaParser.SHEET_PREFIX) | (1 << FormulaParser.ID) | (1 << FormulaParser.FLOAT_NUMBER) | (1 << FormulaParser.INT) | (1 << FormulaParser.STRING) | (1 << FormulaParser.ADD) | (1 << FormulaParser.SUB))) != 0):
                self.state = 49
                self.expr(0)


            self.state = 56
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 52
                    self.match(FormulaParser.T__3)
                    self.state = 53
                    self.expr(0) 
                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==FormulaParser.T__3:
                self.state = 59
                self.match(FormulaParser.T__3)


            self.state = 62
            self.match(FormulaParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(FormulaParser.ID)
            else:
                return self.getToken(FormulaParser.ID, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(FormulaParser.INT)
            else:
                return self.getToken(FormulaParser.INT, i)

        def getRuleIndex(self):
            return FormulaParser.RULE_functionName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionName" ):
                listener.enterFunctionName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionName" ):
                listener.exitFunctionName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionName" ):
                return visitor.visitFunctionName(self)
            else:
                return visitor.visitChildren(self)




    def functionName(self):

        localctx = FormulaParser.FunctionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_functionName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(FormulaParser.ID)
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FormulaParser.ID or _la==FormulaParser.INT:
                self.state = 65
                _la = self._input.LA(1)
                if not(_la==FormulaParser.ID or _la==FormulaParser.INT):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 70
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RangeAddressContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FormulaParser.RULE_rangeAddress

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class OneCellAddressContext(RangeAddressContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.RangeAddressContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def cellAddress(self):
            return self.getTypedRuleContext(FormulaParser.CellAddressContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOneCellAddress" ):
                listener.enterOneCellAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOneCellAddress" ):
                listener.exitOneCellAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOneCellAddress" ):
                return visitor.visitOneCellAddress(self)
            else:
                return visitor.visitChildren(self)


    class ColAddressContext(RangeAddressContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.RangeAddressContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(FormulaParser.ID)
            else:
                return self.getToken(FormulaParser.ID, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterColAddress" ):
                listener.enterColAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitColAddress" ):
                listener.exitColAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColAddress" ):
                return visitor.visitColAddress(self)
            else:
                return visitor.visitChildren(self)


    class RowAddressContext(RangeAddressContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.RangeAddressContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(FormulaParser.INT)
            else:
                return self.getToken(FormulaParser.INT, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRowAddress" ):
                listener.enterRowAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRowAddress" ):
                listener.exitRowAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRowAddress" ):
                return visitor.visitRowAddress(self)
            else:
                return visitor.visitChildren(self)


    class ParensAddressContext(RangeAddressContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.RangeAddressContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def rangeAddress(self):
            return self.getTypedRuleContext(FormulaParser.RangeAddressContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParensAddress" ):
                listener.enterParensAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParensAddress" ):
                listener.exitParensAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParensAddress" ):
                return visitor.visitParensAddress(self)
            else:
                return visitor.visitChildren(self)


    class PairCellAddressContext(RangeAddressContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FormulaParser.RangeAddressContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def cellAddress(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FormulaParser.CellAddressContext)
            else:
                return self.getTypedRuleContext(FormulaParser.CellAddressContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPairCellAddress" ):
                listener.enterPairCellAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPairCellAddress" ):
                listener.exitPairCellAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPairCellAddress" ):
                return visitor.visitPairCellAddress(self)
            else:
                return visitor.visitChildren(self)



    def rangeAddress(self):

        localctx = FormulaParser.RangeAddressContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_rangeAddress)
        try:
            self.state = 86
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = FormulaParser.PairCellAddressContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 71
                self.cellAddress()
                self.state = 72
                self.match(FormulaParser.T__4)
                self.state = 73
                self.cellAddress()
                pass

            elif la_ == 2:
                localctx = FormulaParser.OneCellAddressContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.cellAddress()
                pass

            elif la_ == 3:
                localctx = FormulaParser.ColAddressContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 76
                self.match(FormulaParser.ID)
                self.state = 77
                self.match(FormulaParser.T__4)
                self.state = 78
                self.match(FormulaParser.ID)
                pass

            elif la_ == 4:
                localctx = FormulaParser.RowAddressContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 79
                self.match(FormulaParser.INT)
                self.state = 80
                self.match(FormulaParser.T__4)
                self.state = 81
                self.match(FormulaParser.INT)
                pass

            elif la_ == 5:
                localctx = FormulaParser.ParensAddressContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 82
                self.match(FormulaParser.T__1)
                self.state = 83
                self.rangeAddress()
                self.state = 84
                self.match(FormulaParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CellAddressContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(FormulaParser.ID, 0)

        def INT(self):
            return self.getToken(FormulaParser.INT, 0)

        def getRuleIndex(self):
            return FormulaParser.RULE_cellAddress

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCellAddress" ):
                listener.enterCellAddress(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCellAddress" ):
                listener.exitCellAddress(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCellAddress" ):
                return visitor.visitCellAddress(self)
            else:
                return visitor.visitChildren(self)




    def cellAddress(self):

        localctx = FormulaParser.CellAddressContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_cellAddress)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(FormulaParser.ID)
            self.state = 89
            self.match(FormulaParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT_NUMBER(self):
            return self.getToken(FormulaParser.FLOAT_NUMBER, 0)

        def STRING(self):
            return self.getToken(FormulaParser.STRING, 0)

        def INT(self):
            return self.getToken(FormulaParser.INT, 0)

        def getRuleIndex(self):
            return FormulaParser.RULE_lit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLit" ):
                listener.enterLit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLit" ):
                listener.exitLit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLit" ):
                return visitor.visitLit(self)
            else:
                return visitor.visitChildren(self)




    def lit(self):

        localctx = FormulaParser.LitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_lit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FormulaParser.FLOAT_NUMBER) | (1 << FormulaParser.INT) | (1 << FormulaParser.STRING))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         




