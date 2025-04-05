"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"

class Symbol:
    def __init__(self,name,mtype,value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"

class StaticChecker(BaseVisitor, Utils):

    def __init__(self,ast):
        self.decl_num = 1
        self.ast = ast
        self.global_envi = [
            Symbol("getInt",MType([],IntType()),0),
            Symbol("putInt",MType([IntType()],VoidType()),0),
            Symbol("putIntLn",MType([IntType()],VoidType()),0),
            Symbol("getFloat",MType([],IntType()),0),
            Symbol("putFloat",MType([FloatType()],VoidType()),0),
            Symbol("putFloatLn",MType([FloatType()],VoidType()),0),
            Symbol("getBool",MType([],BoolType()),0),
            Symbol("putBool",MType([BoolType()],VoidType()),0),
            Symbol("putBoolLn",MType([BoolType()],VoidType()),0),
            Symbol("getString",MType([],StringType()),0),
            Symbol("putString",MType([StringType()],VoidType()),0),
            Symbol("putStringLn",MType([StringType()],VoidType()),0),
            Symbol("putLn",MType([],VoidType()),0),
        ]
 
    def check(self):
        return self.visit(self.ast, self.global_envi)
    
    def check_type(self, ltype, rtype):
        if type(ltype) is VoidType:
            return False
        if (type(ltype) is not type(rtype)) and (type(ltype) is not FloatType or type(rtype) is not IntType):
            return False
        if type(ltype) is ArrayType:
            if len(ltype.dimens) != len(rtype.dimens):
                return False
            if (type(ltype.eleType) is not type(rtype.eleType)) and (type(ltype.eleType) is not FloatType or type(rtype.eleType) is not IntType):
                return False
            for i in range(len(ltype.dimens)):
                if type(ltype.dimens[i]) is IntegerType and type(rtype.dimens[i]) is IntegerType:
                    if ltype.dimens[i].value != rtype.dimens[i].value:
                        return False
        return True
    
    def infer(self, item, typ, param):
        for sym in param:
            if sym.name == item.name:
                sym.mtype = typ

    def visitProgram(self, ast:Program, param):
        param = self.global_envi
        for decl in ast.decl:
            if type(decl) in [MType, StructType, InterfaceType]:
                sym = self.lookup(decl.name, param, lambda x: x.name)
                if sym:
                    raise Redeclared(Function(), decl.name) if type(decl) is MType else Redeclared(Type(), decl.name)
                if type(decl) is MType:
                    param.append(Symbol(decl.name, MType([x.parType for x in decl.params], decl.retType), self.decl_num))
                else:
                    param.append(Symbol(decl.name, decl, self.decl_num))
            self.decl_num += 1
        self.decl_num = 1
        for decl in ast.decl:
            self.visit(decl, param)
            self.decl_num += 1
            for sym in param: print(sym)

    def visitVarDecl(self, ast, param):
        sym = self.lookup(ast.varName, param, lambda x: x.name)
        if sym:
            if self.decl_num >= sym.value:
                raise Redeclared(Variable(), ast.varName)
            else:
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is MType else Redeclared(Type(), sym.name)
        var_type, init_type = self.visit(ast.varType, param) if ast.varType else None, None
        if ast.varInit:
            init_type = self.visit(ast.varInit, param)
            if var_type:
                if not self.check_type(var_type, init_type):
                    raise TypeMismatch(ast)
        param.append(Symbol(ast.varName, var_type if var_type else init_type, self.decl_num))

    def visitConstDecl(self, ast, param):
        sym = self.lookup(ast.conName, param, lambda x: x.name)
        if sym:
            if self.decl_num >= sym.value:
                raise Redeclared(Constant(), ast.conName)
            else:
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is FuncDecl else Redeclared(Type(), sym.name)
        const_type, init_type = self.visit(ast.conType, param) if ast.conType else None, None
        if ast.iniExpr:
            init_type = self.visit(ast.iniExpr, param)
            if const_type:
                if not self.check_type(const_type, init_type):
                    raise TypeMismatch(ast)
        param.append(Symbol(ast.conName, const_type if const_type else init_type, self.decl_num))
        
    def visitFuncDecl(self, ast, param):
        o1 = []
        for param_decl in ast.params:
            sym = self.lookup(param_decl.varName, o1, lambda x: x.name)
            if sym:
                raise Redeclared(Parameter(), param_decl.varName)
            o1.append(Symbol(param_decl.varName, param_decl.varType))
        self.visit(ast.body, o1 + param)
    
    def visitMethodDecl(self, ast, param):
        sym = self.lookup(ast.recType, param, lambda x: x.name)
        if sym:
            if type(sym.mtype) is StructType:
                method = self.lookup(ast.fun.name, [x for x, _ in sym.mtype.elements] + sym.mtype.methods, lambda x: x.fun.name)
                if method:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    self.visit(ast.fun, [ast.receiver] + param)
                    sym.methods.append(ast)
            elif type(sym) is InterfaceType:
                count = sum(1 for x in sym.mtype.methods if x.name == ast.fun.name)
                if count == 0:
                    raise Undeclared(Method(), ast.fun.name)
                elif count == 2:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    self.visit(ast.fun, [ast.receiver] + param)
                    sym.methods.append(Prototype(ast.fun.name, [ast.fun.x.parType for x in ast.fun.params], ast.fun.retType))

    def visitPrototype(self, ast, param):
        return ast

    def visitIntType(self, ast, param):
        return IntType()
    
    def visitFloatType(self, ast, param):
        return FloatType()
    
    def visitBoolType(self, ast, param):
        return BoolType()
    
    def visitStringType(self, ast, param):
        return StringType()
    
    def visitVoidType(self, ast, param):
        return VoidType()

    def visitArrayType(self, ast, param):
        for sz in ast.dimens:
            if type(sz) is Id:
                sz_type = self.visit(sz, param)
                if sz_type is not IntegerType:
                    return TypeMismatch(ltype)
        return ast

    def visitStructType(self, ast, param):
        field_list = []
        for field, _ in ast.elements:
            res = self.lookup(field, field_list, lambda x: x)
            if res:
                raise Redeclared(Field(), field)

    def visitInterfaceType(self, ast, param):
        prototype_list = []
        for prototype in ast.methods:
            res = self.lookup(prototype.name, prototype_list, lambda x: x)
            if res:
                raise Redeclared(Prototype(), prototype.name)
            prototype_list.append(prototype)

    def visitBlock(self, ast, param): pass

    def visitBinaryOp(self, ast, param):
        return ast

    def visitIntLiteral(self, ast, param):
        return IntType()
    
    def visitFloatLiteral(self, ast, param):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, param):
        return BoolType()
    
    def visitStringLiteral(self, ast, param):
        return StringType()
    
    def visitId(self,ast,param):
        res = self.lookup(ast.name, param, lambda x: x.name)
        if res is None:
            raise Undeclared(Identifier(), ast.name)
        return res.mtype
