from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):
    def visitProgram(self,ctx:MiniGoParser.ProgramContext):
        return Program([self.visit(i) for i in ctx.decl()])

    def visitDecl(self,ctx:MiniGoParser.DeclContext):
        return self.visit(ctx.getChild(0))

    def visitFuncdecl(self,ctx:MiniGoParser.FuncdeclContext):
        return FuncDecl(ctx.ID().getText(),[],VoidType(),Block([]))
    	
    def visitVardecl(self,ctx:MiniGoParser.VardeclContext):
        ini = self.visit(ctx.exp()) if ctx.exp() else None
        return VarDecl(ctx.ID().getText(),IntType(),ini)
    
    def visitExp(self,ctx:MiniGoParser.ExpContext):
        if ctx.ID(): return Id(ctx.ID().getText())
        elif ctx.INTLIT(): return IntLiteral(int(ctx.INTLIT().getText()))
        return FloatLiteral(float(ctx.FLOATLIT().getText()))

    

