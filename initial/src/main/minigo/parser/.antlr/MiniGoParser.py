# Generated from /Users/nhphung/LocalDocuments/fromMacBookAir1/Monhoc/KS-NNLT/Materials/Assignments/MiniGo/Assignment3/initial/src/main/minigo/parser/MiniGo.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,17,41,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,4,0,12,8,0,
        11,0,12,0,13,1,0,1,0,1,1,1,1,3,1,20,8,1,1,2,1,2,1,2,1,2,1,2,3,2,
        27,8,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,0,0,5,
        0,2,4,6,8,0,1,1,0,10,12,38,0,11,1,0,0,0,2,19,1,0,0,0,4,21,1,0,0,
        0,6,30,1,0,0,0,8,38,1,0,0,0,10,12,3,2,1,0,11,10,1,0,0,0,12,13,1,
        0,0,0,13,11,1,0,0,0,13,14,1,0,0,0,14,15,1,0,0,0,15,16,5,0,0,1,16,
        1,1,0,0,0,17,20,3,6,3,0,18,20,3,4,2,0,19,17,1,0,0,0,19,18,1,0,0,
        0,20,3,1,0,0,0,21,22,5,1,0,0,22,23,5,10,0,0,23,26,5,2,0,0,24,25,
        5,3,0,0,25,27,3,8,4,0,26,24,1,0,0,0,26,27,1,0,0,0,27,28,1,0,0,0,
        28,29,5,4,0,0,29,5,1,0,0,0,30,31,5,5,0,0,31,32,5,10,0,0,32,33,5,
        6,0,0,33,34,5,7,0,0,34,35,5,8,0,0,35,36,5,9,0,0,36,37,5,4,0,0,37,
        7,1,0,0,0,38,39,7,0,0,0,39,9,1,0,0,0,3,13,19,26
    ]

class MiniGoParser ( Parser ):

    grammarFileName = "MiniGo.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'var'", "'int'", "'='", "';'", "'func'", 
                     "'('", "')'", "'{'", "'}'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'\\n'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ID", "INTLIT", "FLOATLIT", 
                      "NL", "WS", "ERROR_CHAR", "ILLEGAL_ESCAPE", "UNCLOSE_STRING" ]

    RULE_program = 0
    RULE_decl = 1
    RULE_vardecl = 2
    RULE_funcdecl = 3
    RULE_exp = 4

    ruleNames =  [ "program", "decl", "vardecl", "funcdecl", "exp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    ID=10
    INTLIT=11
    FLOATLIT=12
    NL=13
    WS=14
    ERROR_CHAR=15
    ILLEGAL_ESCAPE=16
    UNCLOSE_STRING=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MiniGoParser.EOF, 0)

        def decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniGoParser.DeclContext)
            else:
                return self.getTypedRuleContext(MiniGoParser.DeclContext,i)


        def getRuleIndex(self):
            return MiniGoParser.RULE_program




    def program(self):

        localctx = MiniGoParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 10
                self.decl()
                self.state = 13 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==5):
                    break

            self.state = 15
            self.match(MiniGoParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcdecl(self):
            return self.getTypedRuleContext(MiniGoParser.FuncdeclContext,0)


        def vardecl(self):
            return self.getTypedRuleContext(MiniGoParser.VardeclContext,0)


        def getRuleIndex(self):
            return MiniGoParser.RULE_decl




    def decl(self):

        localctx = MiniGoParser.DeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_decl)
        try:
            self.state = 19
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 17
                self.funcdecl()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                self.vardecl()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VardeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MiniGoParser.ID, 0)

        def exp(self):
            return self.getTypedRuleContext(MiniGoParser.ExpContext,0)


        def getRuleIndex(self):
            return MiniGoParser.RULE_vardecl




    def vardecl(self):

        localctx = MiniGoParser.VardeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_vardecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self.match(MiniGoParser.T__0)
            self.state = 22
            self.match(MiniGoParser.ID)
            self.state = 23
            self.match(MiniGoParser.T__1)
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 24
                self.match(MiniGoParser.T__2)
                self.state = 25
                self.exp()


            self.state = 28
            self.match(MiniGoParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncdeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MiniGoParser.ID, 0)

        def getRuleIndex(self):
            return MiniGoParser.RULE_funcdecl




    def funcdecl(self):

        localctx = MiniGoParser.FuncdeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_funcdecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(MiniGoParser.T__4)
            self.state = 31
            self.match(MiniGoParser.ID)
            self.state = 32
            self.match(MiniGoParser.T__5)
            self.state = 33
            self.match(MiniGoParser.T__6)
            self.state = 34
            self.match(MiniGoParser.T__7)
            self.state = 35
            self.match(MiniGoParser.T__8)
            self.state = 36
            self.match(MiniGoParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MiniGoParser.ID, 0)

        def INTLIT(self):
            return self.getToken(MiniGoParser.INTLIT, 0)

        def FLOATLIT(self):
            return self.getToken(MiniGoParser.FLOATLIT, 0)

        def getRuleIndex(self):
            return MiniGoParser.RULE_exp




    def exp(self):

        localctx = MiniGoParser.ExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_exp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7168) != 0)):
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





