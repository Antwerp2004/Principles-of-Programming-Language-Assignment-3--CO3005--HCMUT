"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"

class StaticChecker(BaseVisitor,Utils):
        
    
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [Symbol("getInt",MType([],IntType())),Symbol("putIntLn",MType([IntType()],VoidType()))]
 
    
    def check(self):
        return self.visit(self.ast,self.global_envi)

    def visitProgram(self,ast, c):
        reduce(lambda acc,ele: [self.visit(ele,acc)] + acc , ast.decl,c)
        return c

    def visitVarDecl(self, ast, c):
        res = self.lookup(ast.varName, c, lambda x: x.name)
        if not res is None:
            raise Redeclared(Variable(), ast.varName) 
        if ast.varInit:
            initType = self.visit(ast.varInit, c)
            if ast.varType is None:
                ast.varType = initType
            if not type(ast.varType) is type(initType):
                raise TypeMismatch(ast)
        return Symbol(ast.varName, ast.varType,None)
        

    def visitFuncDecl(self,ast, c):
        res = self.lookup(ast.name, c, lambda x: x.name)
        if not res is None:
            raise Redeclared(Function(), ast.name)
        return Symbol(ast.name, MType([], ast.retType))

    def visitIntLiteral(self,ast, c):
        return IntType()
    
    def visitFloatLiteral(self,ast, c):
        return FloatType()
    
    def visitId(self,ast,c):
        res = self.lookup(ast.name, c, lambda x: x.name)
        if res is None:
            raise Undeclared(Identifier(), ast.name)
        return res.mtype
