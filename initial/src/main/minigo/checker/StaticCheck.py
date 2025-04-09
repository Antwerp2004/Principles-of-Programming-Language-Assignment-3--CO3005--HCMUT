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


def flatten(dat: NestedList):
    if isinstance(dat, list):
        result = []
        for item in dat:
            result.extend(flatten(item))
        return result
    else:
        return [dat]

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
        self.flag_expr = 0
 

    def check(self):
        return self.visit(self.ast, self.global_envi)


    def check_type(self, ltype, rtype, param):
        if ltype is None or rtype is None:
            return True
        
        elif type(ltype) is not type(rtype):
            if type(ltype) is FloatType and type(rtype) is IntType:
                return True
            elif type(ltype) is InterfaceType and type(rtype) is StructType:
                for i in range(len(ltype.methods)):
                    res = self.lookup(ltype.methods[i].name, rtype.methods, lambda x: x.fun.name)
                    if res is None:
                        return False
                    for j in range (len(ltype.methods[i].params)):
                        if not self.check_exact_type(self.visit(ltype.methods[i].params[j], param), self.visit(res.fun.params[j].parType, param), param):
                            return False
                    if not self.check_exact_type(self.visit(ltype.methods[i].retType, param), self.visit(res.fun.retType, param), param):
                        return False
                return True
            return False
        
        elif type(ltype) is ArrayType:
            if len(ltype.dimens) != len(rtype.dimens):
                return False
            eleType_left = self.visit(ltype.eleType, param)
            eleType_right = self.visit(rtype.eleType, param)
            if not self.check_exact_type(eleType_left, eleType_right, param) and (type(eleType_left) is not FloatType or type(eleType_right) is not IntType):
                return False
            for i in range(len(ltype.dimens)):
                if type(ltype.dimens[i]) is IntLiteral and type(rtype.dimens[i]) is IntLiteral:
                    if ltype.dimens[i].value != rtype.dimens[i].value:
                        return False
                    
        elif type(ltype) is StructType or type(ltype) is InterfaceType:
            # print(ltype, rtype)
            if ltype.name != rtype.name:
                return False
        return True
    

    def check_exact_type(self, ltype, rtype, param):
        if type(ltype) is not type(rtype):
            return False
        
        elif type(ltype) is ArrayType:
            if len(ltype.dimens) != len(rtype.dimens):
                return False
            eleType_left = self.visit(ltype.eleType, param)
            eleType_right = self.visit(rtype.eleType, param)
            if not self.check_exact_type(eleType_left, eleType_right, param):
                return False
            for i in range(len(ltype.dimens)):
                if type(ltype.dimens[i]) is IntLiteral and type(rtype.dimens[i]) is IntLiteral:
                    if ltype.dimens[i].value != rtype.dimens[i].value:
                        return False
                    
        elif ltype != rtype:
            return False
        return True


    def visitProgram(self, ast:Program, param): 
        param = self.global_envi
        for decl in ast.decl:
            if type(decl) is MethodDecl:
                continue
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
            if sym.value is None or self.decl_num >= sym.value:
                raise Redeclared(Variable(), ast.varName)
            else:
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is MType else Redeclared(Type(), sym.name)

        var_type, init_type = self.visit(ast.varType, param) if ast.varType else None, None
        if ast.varInit:
            self.flag_expr = 1
            init_type = self.visit(ast.varInit, param)
            self.flag_expr = 0
            if var_type:
                if not self.check_type(var_type, init_type, param):
                    raise TypeMismatch(ast)
        param.append(Symbol(ast.varName, ast.varType if ast.varType else init_type, self.decl_num))
        # for sym in param: print(sym)


    def visitConstDecl(self, ast, param): # Haven't caluculated the value of the constant
        sym = self.lookup(ast.conName, param, lambda x: x.name)
        if sym:
            if self.decl_num >= sym.value:
                raise Redeclared(Constant(), ast.conName)
            else:
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is MType else Redeclared(Type(), sym.name)
        self.flag_expr = 1
        init_type = self.visit(ast.iniExpr, param)
        self.flag_expr = 0
        param.append(Symbol(ast.conName, init_type, self.decl_num))
        

    def visitFuncDecl(self, ast, param):
        o = []
        for param_decl in ast.params:
            sym = self.lookup(param_decl.parName, o, lambda x: x.name)
            if sym:
                raise Redeclared(Parameter(), param_decl.parName)
            o.append(Symbol(param_decl.parName, param_decl.parType))
        ret, idx = self.visit(ast.body, o + param), 0
        for stmt in ast.body.member:
            if type(stmt) is Return:
                if not self.check_exact_type(ret[idx], self.visit(ast.retType, param), param):
                    raise TypeMismatch(stmt) 
                idx += 1           
    

    def visitMethodDecl(self, ast, param):
        sym = self.lookup(ast.recType.name, param, lambda x: x.name)
        if sym:
            if type(sym.mtype) is StructType:
                res = self.lookup(ast.fun.name, sym.mtype.methods, lambda x: x.fun.name)
                if res:
                    raise Redeclared(Method(), ast.fun.name)
                res = self.lookup(ast.fun.name, [x for x, _ in sym.mtype.elements], lambda x: x)
                if res:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    sym.mtype.methods.append(ast)
                    self.visit(ast.fun, [Symbol(ast.receiver, ast.recType)] + param)

            elif type(sym.mtype) is InterfaceType:
                count = sum(1 for x in sym.mtype.methods if x.name == ast.fun.name)
                if count == 0:
                    raise Undeclared(Method(), ast.fun.name)
                elif count == 2:
                    raise Redeclared(Method(), ast.fun.name)
                else:
                    sym.mtype.methods.append(AST.Prototype(ast.fun.name, [ast.fun.x.parType for x in ast.fun.params], ast.fun.retType))
                    self.visit(ast.fun, [Symbol(ast.receiver, Id(self.visit(ast.recType, param).name))] + param)


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
            if type(sz_type) is not IntType:
                return TypeMismatch(ast)
        return ast


    def visitStructType(self, ast, param):
        field_list = []
        for field, _ in ast.elements:
            res = self.lookup(field, field_list, lambda x: x)
            if res:
                raise Redeclared(Field(), field)
            field_list.append(field)
        return ast


    def visitInterfaceType(self, ast, param):
        prototype_list = []
        for prototype in ast.methods:
            res = self.lookup(prototype.name, prototype_list, lambda x: x)
            if res:
                raise Redeclared(Prototype(), prototype.name)
            prototype_list.append(prototype.name)
        return ast


    def visitBlock(self, ast, param):
        o, ret = [], []
        # for sym in param: print(sym)
        for stmt in ast.member:
            if type(stmt) is VarDecl:
                sym = self.lookup(stmt.varName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Variable(), stmt.varName)
                var_type, init_type = self.visit(stmt.varType, o + param) if stmt.varType else None, None
                if stmt.varInit:
                    self.flag_expr = 1
                    init_type = self.visit(stmt.varInit, o + param)
                    if var_type:
                        if not self.check_type(var_type, init_type, o + param):
                            raise TypeMismatch(stmt)
                    self.flag_expr = 0
                o.append(Symbol(stmt.varName, stmt.varType if stmt.varType else init_type))

            elif type(stmt) is ConstDecl:
                sym = self.lookup(stmt.conName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Constant(), stmt.conName)
                self.flag_expr = 1
                init_type = self.visit(stmt.iniExpr, o + param)
                self.flag_expr = 0
                o.append(Symbol(stmt.conName, init_type))
            
            elif type(stmt) is Assign:
                lhs_type = self.visit(stmt, o + param)
                if not lhs_type:
                    self.flag_expr = 1
                    o.append(Symbol(stmt.lhs.name, self.visit(stmt.rhs, o + param)))
                    self.flag_expr = 0

            elif type(stmt) is Return:
                ret.append(self.visit(stmt, o + param))

            else:
                self.visit(stmt, o + param)
        return ret


    def visitAssign(self, ast, param):
        # for sym in param: print(sym)
        self.flag_expr = 1
        rhs_type, lhs_type = self.visit(ast.rhs, param), None
        self.flag_expr = 0
        if type(ast.lhs) is not Id:
            self.flag_expr = 1
            lhs_type = self.visit(ast.lhs, param)
            self.flag_expr = 0
        else:
            res = self.lookup(ast.lhs.name, param, lambda x: x.name)
            if res:
                lhs_type = self.visit(res.mtype, param) if type(res.mtype) is not MType else res.mtype
        if not self.check_type(lhs_type, rhs_type, param):
            raise TypeMismatch(ast)
        # print("LHS type: ", lhs_type)
        return lhs_type


    def visitIf(self, ast, param):
        # Condition
        self.flag_expr = 1
        condition_type = self.visit(ast.expr, param)
        self.flag_expr = 0
        if type(condition_type) is not BoolType:
            raise TypeMismatch(ast)
        # Then
        self.visit(ast.thenStmt, param)
        # Else
        if ast.elseStmt:
            self.visit(ast.elseStmt, param)


    def visitForBasic(self, ast, param):
        # Condition
        self.flag_expr = 1
        condition_type = self.visit(ast.cond, param)
        self.flag_expr = 0
        if type(condition_type) is not BoolType:
            raise TypeMismatch(ast)
        # Loop body
        self.visit(ast.loop, param)


    def visitForStep(self, ast, param):
        o = []
        # Initialization
        if type(ast.init) is VarDecl:
            var_type = self.visit(ast.init.varType, o + param) if ast.init.varType else None
            self.flag_expr = 1
            init_type = self.visit(ast.init.varInit, o + param)
            self.flag_expr = 0
            if var_type:
                if not self.check_type(var_type, init_type, o + param):
                    raise TypeMismatch(ast.init)
            o.append(Symbol(ast.init.varName, ast.init.varType if ast.init.varType else init_type))
        elif type(ast.init) is Assign:
            lhs_type = self.visit(ast.init, o + param)
            if not lhs_type:
                self.flag_expr = 1
                o.append(Symbol(ast.init.lhs.name, self.visit(ast.init.rhs, o + param)))
                self.flag_expr = 0
        
        # Condition
        self.flag_expr = 1
        condition_type = self.visit(ast.cond, o + param)
        self.flag_expr = 0
        if type(condition_type) is not BoolType:
            raise TypeMismatch(ast)
        
        # Update
        lhs_type = self.visit(ast.upda, o + param)
        if not lhs_type:
            self.flag_expr = 1
            o.append(Symbol(ast.upda.lhs.name, self.visit(ast.upda.rhs, o + param)))
            self.flag_expr = 0
        
        # Loop body
        for stmt in ast.loop.member:
            if type(stmt) is VarDecl:
                sym = self.lookup(stmt.varName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Variable(), stmt.varName)
                var_type, init_type = self.visit(stmt.varType, o + param) if stmt.varType else None, None
                if stmt.varInit:
                    self.flag_expr = 1
                    init_type = self.visit(stmt.varInit, o + param)
                    self.flag_expr = 0
                    if var_type:
                        if not self.check_type(var_type, init_type, o + param):
                            raise TypeMismatch(stmt)
                o.append(Symbol(stmt.varName, stmt.varType if stmt.varType else init_type))

            elif type(stmt) is ConstDecl:
                sym = self.lookup(stmt.conName, o, lambda x: x.name)
                if sym:
                    raise Redeclared(Constant(), stmt.conName)
                self.flag_expr = 1
                init_type = self.visit(stmt.iniExpr, o + param)
                self.flag_expr = 0
                o.append(Symbol(stmt.conName, init_type))
            
            elif type(stmt) is Assign:
                lhs_type = self.visit(stmt, o + param)
                if not lhs_type:
                    self.flag_expr = 1
                    o.append(Symbol(stmt.lhs.name, self.visit(stmt.rhs, o + param)))
                    self.flag_expr = 0

            else:
                self.visit(stmt, o + param)


    def visitForEach(self, ast, param):
        index_type, value_type = None, self.visit(ast.value, param)
        if ast.idx.name != '_':
            index_type = self.visit(ast.idx, param)
        if index_type and type(index_type) is not IntType:
            raise TypeMismatch(ast)
        self.flag_expr = 1
        arr_type = self.visit(ast.arr, param)
        self.flag_expr = 0
        if type(arr_type) is not ArrayType:
            raise TypeMismatch(ast)
        if type(self.visit(arr_type.eleType, param)) is not type(value_type):
            raise TypeMismatch(ast)
        # Loop body
        self.visit(ast.loop, param)
    

    def visitContinue(self, ast, param):
        pass

    
    def visitBreak(self, ast, param):
        pass


    def visitReturn(self, ast, param):
        return_type = VoidType()
        if ast.expr:
            self.flag_expr = 1
            return_type = self.visit(ast.expr, param)
        self.flag_expr = 0
        return return_type


    def visitBinaryOp(self, ast, param):
        # for sym in param: print(sym)
        self.flag_expr = 1
        ltype = self.visit(ast.left, param)
        rtype = self.visit(ast.right, param)
        if ast.op == '+':
            if type(ltype) is IntType and type(rtype) is IntType:
                return IntType()
            elif type(ltype) is FloatType and type(rtype) is FloatType:
                return FloatType()
            elif type(ltype) is StringType and type(rtype) is StringType:
                return StringType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['-', '*', '/']:
            if type(ltype) is IntType and type(rtype) is IntType:
                return IntType()
            elif type(ltype) is FloatType and type(rtype) is FloatType:
                return FloatType()
            elif (type(ltype) is IntType and type(rtype) is FloatType) or (type(ltype) is FloatType and type(rtype) is IntType):
                return FloatType()
            else:
                raise TypeMismatch(ast)
        elif ast.op == '%':
            if type(ltype) is IntType and type(rtype) is IntType:
                return IntType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['==', '!=', '<', '>', '<=', '>=']:
            if type(ltype) is IntType and type(rtype) is IntType:
                return BoolType()
            elif type(ltype) is FloatType and type(rtype) is FloatType:
                return BoolType()
            elif type(ltype) is StringType and type(rtype) is StringType:
                return BoolType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['&&', '||']:
            if type(ltype) is BoolType and type(rtype) is BoolType:
                return BoolType()
            else:
                raise TypeMismatch(ast)
        self.flag_expr = 0
            

    def visitUnaryOp(self, ast, param):
        self.flag_expr = 1
        body_type = self.visit(ast.body, param)
        if ast.op == '-':
            if type(body_type) is IntType:
                return IntType()
            elif type(body_type) is FloatType:
                return FloatType()
            else:
                raise TypeMismatch(ast)
        elif ast.op == '!':
            if type(body_type) is BoolType:
                return BoolType()
            else:
                raise TypeMismatch(ast)
        self.flag_expr = 0
    

    def visitFuncCall(self, ast, param):
        func_type = self.lookup(ast.funName, param, lambda x: x.name)
        if func_type is None:
            raise Undeclared(Function(), ast.funName)
        if len(ast.args) != len(func_type.mtype.partype):
            raise TypeMismatch(ast)
        tmp = self.flag_expr
        self.flag_expr = 1
        for i in range(0, len(ast.args)):
            arg_type = self.visit(ast.args[i], param)
            func_type_arg = self.visit(func_type.mtype.partype[i], param)
            print(func_type_arg, arg_type)
            if not self.check_exact_type(arg_type, func_type_arg, param):
                raise TypeMismatch(ast)
        self.flag_expr = tmp
        return_type = self.visit(func_type.mtype.rettype, param)
        if type(return_type) is VoidType and self.flag_expr == 1:
            raise TypeMismatch(ast)
        elif type(return_type) is not VoidType and self.flag_expr == 0:
            raise TypeMismatch(ast)
        return return_type
            
    
    def visitMethCall(self, ast, param):
        # for sym in param: print(sym)
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
                if not self.check_exact_type(arg_type, method_type_arg, param):
                    raise TypeMismatch(ast)
            return_type = self.visit(method.fun.retType, param)
            if type(return_type) is VoidType and self.flag_expr == 1:
                raise TypeMismatch(ast)
            elif type(return_type) is not VoidType and self.flag_expr == 0:
                raise TypeMismatch(ast)
            return return_type
                
        elif type(receiver) is InterfaceType:
            method = self.lookup(ast.metName, receiver.methods, lambda x: x.name)
            if method is None:
                raise Undeclared(Method(), ast.metName)
            if len(ast.args) != len(method.params):
                raise TypeMismatch(ast)
            for i in range(len(ast.args)):
                arg_type = self.visit(ast.args[i], param)
                method_type_arg = self.visit(method.params[i], param)
                if not self.check_exact_type(arg_type, method_type_arg, param):
                    raise TypeMismatch(ast)
            return_type = self.visit(method.retType, param)
            if type(return_type) is VoidType and self.flag_expr == 1:
                raise TypeMismatch(ast)
            elif type(return_type) is not VoidType and self.flag_expr == 0:
                raise TypeMismatch(ast)
            return return_type
    

    def visitId(self,ast,param):
        res = self.lookup(ast.name, param, lambda x: x.name)
        if res is None:
            raise Undeclared(Identifier(), ast.name)
        return self.visit(res.mtype, param)


    def visitArrayCell(self, ast, param):
        self.flag_expr = 1
        arr_type = self.visit(ast.arr, param)
        if type(arr_type) is not ArrayType:
            raise TypeMismatch(ast)
        for idx in ast.idx:
            idx_type = self.visit(idx, param)
            if type(idx_type) is not IntType:
                raise TypeMismatch(ast)
        self.flag_expr = 0
        return self.visit(arr_type.eleType, param)


    def visitFieldAccess(self, ast, param):
        self.flag_expr = 1
        recType = self.visit(ast.receiver, param)
        if type(recType) is not StructType:
            # print ("Hello")
            raise TypeMismatch(ast)
        # print ("Hello")
        res = self.lookup(ast.field, recType.elements, lambda x: x[0])
        if res is None:
            raise Undeclared(Field(), ast.field)
        self.flag_expr = 0
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
        self.flag_expr = 1
        for sz in ast.dimens:
            sz_type = self.visit(sz, param)
            if type(sz_type) is not IntType:
                raise TypeMismatch(ast)
        array_ele_type = self.visit(ast.eleType, param)
        ele_list = flatten(ast.value)
        for ele in ele_list:
            ele_type = self.visit(ele, param)
            if not self.check_exact_type(ele_type, array_ele_type, param):
                raise TypeMismatch(ast)
        self.flag_expr = 0
        return ArrayType(ast.dimens, ast.eleType)


    def visitStructLiteral(self, ast, param):
        self.flag_expr = 1
        struct_type = self.lookup(ast.name, param, lambda x: x.name)
        for ele in ast.elements:
            res = self.lookup(ele[0], struct_type.mtype.elements, lambda x: x[0])
            if res is None:
                raise Undeclared(Field(), ele[0])
            ele_type = self.visit(ele[1], param)
            if not self.check_exact_type(ele_type, self.visit(res[1], param), param):
                raise TypeMismatch(ast)
        self.flag_expr = 0
        return struct_type.mtype
    

    def visitNilLiteral(self, ast, param):
        pass