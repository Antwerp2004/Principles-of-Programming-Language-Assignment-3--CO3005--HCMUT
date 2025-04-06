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
        
        if (type(ltype) is not type(rtype)):
            if type(ltype) is FloatType and type(rtype) is IntType:
                return True
            elif type(ltype) is InterfaceType and type(rtype) is StructType:
                for i in range(len(ltype.methods)):
                    res = self.lookup(ltype.methods[i].name, rtype.methods, lambda x: x.fun.name)
                    if res is None:
                        return False
                    for j in range (len(ltype.methods[i].params)):
                        if type(self.visit(ltype.methods[i].params[j], params)) is not type(self.visit(res.fun.params[j].parType, params)):
                            return False
                    if type(self.visit(ltype.methods[i].retType, params)) is not type(self.visit(res.fun.retType, params)):
                        return False
                return True
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
                    
        elif tpye(ltype) is StructType or type(ltype) is InterfaceType:
            if ltype.name != rtype.name:
                return False
        return True


    def visitProgram(self, ast:Program, param):
        param = self.global_envi
        for decl in ast.decl and type(decl) is not MethodDecl:
            if type(decl) in [FuncDecl, StructType, InterfaceType]:
                sym = self.lookup(decl.name, param, lambda x: x.name)
                if sym:
                    raise Redeclared(Function(), decl.name) if type(decl) is FuncDecl else Redeclared(Type(), decl.name)
                if type(decl) is FuncDecl:
                    param.append(Symbol(decl.name, MType([x.parType for x in decl.params], decl.retType), self.decl_num))
                else:
                    param.append(Symbol(decl.name, decl, self.decl_num))
            self.decl_num += 1

        for decl in ast.decl:
            if type(decl) is MethodDecl:
                self.visit(decl, param)

        self.decl_num = 1
        for decl in ast.decl:
            if type(decl) is not MethodDecl:
                self.visit(decl, param)
                self.decl_num += 1


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
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is MType else Redeclared(Type(), sym.name)

        const_type, init_type = self.visit(ast.conType, param) if ast.conType else None, None
        if ast.iniExpr:
            init_type = self.visit(ast.iniExpr, param)
            if const_type:
                if not self.check_type(const_type, init_type):
                    raise TypeMismatch(ast)
        param.append(Symbol(ast.conName, const_type if const_type else init_type, self.decl_num))
        

    def visitFuncDecl(self, ast, param):
        o = []
        for param_decl in ast.params:
            sym = self.lookup(param_decl.varName, o, lambda x: x.name)
            if sym:
                raise Redeclared(Parameter(), param_decl.varName)
            o.append(Symbol(param_decl.varName, param_decl.varType))
        self.visit(ast.body, o + param)
    

    def visitMethodDecl(self, ast, param):
        typ = self.visit(ast.recType, param)
        sym = self.lookup(typ.name, param, lambda x: x.name)
        if sym:
            if type(sym.mtype) is StructType:
                method = self.lookup(ast.fun.name, [x for x, _ in sym.mtype.elements] + sym.mtype.methods, lambda x: x.fun.name)
                if method:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    self.visit(ast.fun, [ast.receiver] + param)
                    sym.methods.append(ast)

            elif type(sym.mtype) is InterfaceType:
                count = sum(1 for x in sym.mtype.methods if x.name == ast.fun.name)
                if count == 0:
                    raise Undeclared(Method(), ast.fun.name)
                elif count == 2:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    self.visit(ast.fun, [ast.receiver] + param)
                    sym.mtype.methods.append(AST.Prototype(ast.fun.name, [ast.fun.x.parType for x in ast.fun.params], ast.fun.retType))


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
            prototype_list.append(prototype.name)


    def visitBlock(self, ast, param):
        o = []
        for stmt in ast.member:
            if type(stmt) is VarDecl:
                sym = self.lookup(stmt.varName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Variable(), stmt.varName)
                var_type, init_type = self.visit(stmt.varType, param) if stmt.varType else None, None
                if stmt.varInit:
                    init_type = self.visit(stmt.varInit, param)
                    if var_type:
                        if not self.check_type(var_type, init_type):
                            raise TypeMismatch(stmt)
                o.append(Symbol(stmt.varName, var_type if var_type else init_type)) 

            elif type(stmt) is ConstDecl:
                sym = self.lookup(stmt.conName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Constant(), stmt.conName)
                const_type, init_type = self.visit(stmt.conType, param) if stmt.conType else None, None
                if stmt.iniExpr:
                    init_type = self.visit(stmt.iniExpr, param)
                    if const_type:
                        if not self.check_type(const_type, init_type):
                            raise TypeMismatch(stmt)
                o.append(Symbol(stmt.conName, const_type if const_type else init_type))
            
            elif type(stmt) is Assign:
                self.visit(stmt, o + param)


    def visitAssign(self, ast, param):
        lhs_type = self.visit(ast.lhs, param)
        rhs_type = self.visit(ast.rhs, param)
        if not self.check_type(lhs_type, rhs_type):
            raise TypeMismatch(ast)


    def visitBinaryOp(self, ast, param):
        return ast
    

    def visitFuncCall(self, ast, param):
        func_type = self.lookup(ast.funName, param, lambda x: x.name)
        if func_type is None:
            raise Undeclared(Function(), ast.funName)
        if len(ast.args) != len(func_type.mtype.partype):
            raise TypeMismatch(ast)
        for i in range(len(ast.args)):
            arg_type = self.visit(ast.args[i], param)
            func_type_arg = self.visit(func_type.mtype.partype[i], param)
            if arg_type != func_type_arg:
                raise TypeMismatch(ast)
            
    
    def visitMethodCall(self, ast, param):
        receiver = self.visit(ast.receiver, param)
        if type(receiver) is not StructType and type(receiver) is not InterfaceType:
            raise TypeMismatch(ast)
        elif type(receiver) is StructType:
            method = self.lookup(ast.metName, receiver.methods, lambda x: x.fun.name)
            if method is None:
                raise Undeclared(Method(), ast.metName)
            if len(ast.args) != len(method.fun.params):
                raise TypeMismatch(ast)
            for i in range(len(ast.args)):
                arg_type = self.visit(ast.args[i], param)
                method_type_arg = self.visit(method.fun.params[i].parType, param)
                if arg_type != method_type_arg:
                    raise TypeMismatch(ast)
                
        elif type(receiver) is InterfaceType:
            method = self.lookup(ast.metName, receiver.methods, lambda x: x.name)
            if method is None:
                raise Undeclared(Method(), ast.metName)
            if len(ast.args) != len(method.params):
                raise TypeMismatch(ast)
            for i in range(len(ast.args)):
                arg_type = self.visit(ast.args[i], param)
                method_type_arg = self.visit(method.params[i], param)
                if arg_type != method_type_arg:
                    raise TypeMismatch(ast)
    

    def visitId(self,ast,param):
        res = self.lookup(ast.name, param, lambda x: x.name)
        if res is None:
            raise Undeclared(Identifier(), ast.name)
        return res.mtype


    def visitArrayCell(self, ast, param):
        arr_type = self.visit(ast.arr, param)
        if type(arr_type) is not ArrayType:
            raise TypeMismatch(ast)
        for idx in ast.idx:
            idx_type = self.visit(idx, param)
            if type(idx_type) is not IntType:
                raise TypeMismatch(ast)
        return arr_type


    def visitFieldAccess(self, ast, param):
        recType = self.visit(ast.receiver, param)
        if type(recType) is not StructType:
            raise TypeMismatch(ast)
        res = self.lookup(ast.field, recType.elements, lambda x: x[0])
        if res is None:
            raise Undeclared(Field(), ast.field)
        return self.visit(res[1], param)


    def visitIntLiteral(self, ast, param):
        return IntType()


    def visitFloatLiteral(self, ast, param):
        return FloatType()


    def visitBooleanLiteral(self, ast, param):
        return BoolType()


    def visitStringLiteral(self, ast, param):
        return StringType()
    

    def visitArrayLiteral(self, ast, param):
        for sz in ast.dimens:
            sz_type = self.visit(sz, param)
            if sz_type is not IntegerType:
                return TypeMismatch(ltype)
        array_type = self.visit(ast.eleType, param)


    def visitStructLiteral(self, ast, param):
        struct_type = self.visit(ast.name, param)
        for ele in ast.elements:
            res = self.lookup(ele[0], struct_type.elements, lambda x: x[0])
            if res is None:
                raise Undeclared(Field(), ele[0])
        return struct_type
    

    def visitNilLiteral(self, ast, param):
        return VoidType()