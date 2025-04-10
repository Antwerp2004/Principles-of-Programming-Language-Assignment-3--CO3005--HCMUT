"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce
import operator


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"
    

class Symbol:
    def __init__(self, name, mtype, value=None, decl_num=None):
        self.name = name
        self.mtype = mtype
        self.value = value
        self.decl_num = decl_num

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ("" if self.decl_num is None else "," + str(self.decl_num)) + ")"


def flatten(dat: NestedList):

    if isinstance(dat, list):
        result = []
        for item in dat:
            result.extend(flatten(item))
        return result
    else:
        return [dat]
    

ops = {
    # Unary operators (right-to-left associativity)
    '!': operator.not_,      # logical NOT
    '-u': operator.neg,      # unary minus
    
    # Binary operators with precedence 3 (left-to-right)
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    
    # Binary operators with precedence 4 (left-to-right)
    '+': operator.add,
    '-': operator.sub,
    
    # Binary comparison operators with precedence 5 (left-to-right)
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    
    # Logical AND with precedence 6 (left-to-right)
    '&&': lambda a, b: a and b,
    
    # Logical OR with precedence 7 (left-to-right)
    '||': lambda a, b: a or b,
}


class StaticChecker(BaseVisitor, Utils):

    def __init__(self,ast):
        self.decl_num = 1
        self.ast = ast
        self.global_envi = [
            Symbol("getInt",MType([],IntType()),None,0),
            Symbol("putInt",MType([IntType()],VoidType()),None,0),
            Symbol("putIntLn",MType([IntType()],VoidType()),None,0),
            Symbol("getFloat",MType([],IntType()),None,0),
            Symbol("putFloat",MType([FloatType()],VoidType()),None,0),
            Symbol("putFloatLn",MType([FloatType()],VoidType()),None,0),
            Symbol("getBool",MType([],BoolType()),None,0),
            Symbol("putBool",MType([BoolType()],VoidType()),None,0),
            Symbol("putBoolLn",MType([BoolType()],VoidType()),None,0),
            Symbol("getString",MType([],StringType()),None,0),
            Symbol("putString",MType([StringType()],VoidType()),None,0),
            Symbol("putStringLn",MType([StringType()],VoidType()),None,0),
            Symbol("putLn",MType([],VoidType()),None,0),
        ]
        self.flag_expr = 0
        self.flag_func = None
 

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
                left_sz, right_sz = None, None
                if type(ltype.dimens[i]) is IntLiteral:
                    left_sz = ltype.dimens[i].value
                else:
                    res = self.lookup(ltype.dimens[i].name, param, lambda x: x.name)
                    left_sz = res.value
                if type(rtype.dimens[i]) is IntLiteral:
                    right_sz = rtype.dimens[i].value
                else:
                    res = self.lookup(rtype.dimens[i].name, param, lambda x: x.name)
                    right_sz = res.value
                if int(left_sz) != int(right_sz):
                    return False
                    
        elif type(ltype) is StructType or type(ltype) is InterfaceType:
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
                left_sz, right_sz = None, None
                if type(ltype.dimens[i]) is IntLiteral:
                    left_sz = ltype.dimens[i].value
                else:
                    res = self.lookup(ltype.dimens[i].name, param, lambda x: x.name)
                    left_sz = res.value
                if type(rtype.dimens[i]) is IntLiteral:
                    right_sz = rtype.dimens[i].value
                else:
                    res = self.lookup(rtype.dimens[i].name, param, lambda x: x.name)
                    right_sz = res.value
                if int(left_sz) != int(right_sz):
                    return False
         
        elif ltype != rtype:
            return False
        
        return True
    

    def cal_const(self, ast, param):
        if type(ast) is BinaryOp:
            if ast.op in ['+', '-', '*', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||']:
                return ops[ast.op](self.cal_const(ast.left, param), self.cal_const(ast.right, param))
            elif ast.op == '/':
                if type(ast.left) is IntLiteral:
                    return self.cal_const(ast.left, param) // self.cal_const(ast.right, param)
                else:
                    return self.cal_const(ast.left, param) / self.cal_const(ast.right, param)
        
        elif type(ast) is UnaryOp:
            if ast.op == '-':
                return ops['-u'](self.cal_const(ast.body, param))
            elif ast.op == '!':
                return ops['!'](self.cal_const(ast.body, param))
        
        elif type(ast) in [IntLiteral, FloatLiteral, StringLiteral, BooleanLiteral]:
            return ast.value
        
        elif type(ast) is Id:
            res = self.lookup(ast.name, param, lambda x: x.name)
            if res is None:
                raise Undeclared(Identifier(), ast.name)
            return res.value
        
        else:
            return ast
    

    def check_Type(self, comp_type):
        if type(comp_type.mtype) is StructType or type(comp_type.mtype) is InterfaceType:
            if comp_type.decl_num is not None:
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
                    param.append(Symbol(decl.name, MType([x.parType for x in decl.params], decl.retType), None, self.decl_num))
                else:
                    param.append(Symbol(decl.name, decl, None, self.decl_num))
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
            if sym.decl_num is None or self.decl_num >= sym.decl_num:
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
        param.append(Symbol(ast.varName, ast.varType if ast.varType else init_type, None, self.decl_num))


    def visitConstDecl(self, ast, param):
        sym = self.lookup(ast.conName, param, lambda x: x.name)
        if sym:
            if self.decl_num >= sym.decl_num:
                raise Redeclared(Constant(), ast.conName)
            else:
                raise Redeclared(Function(), sym.name) if type(sym.mtype) is MType else Redeclared(Type(), sym.name)
        self.flag_expr = 1
        init_type = self.visit(ast.iniExpr, param)
        self.flag_expr = 0
        const_value = self.cal_const(ast.iniExpr, param)
        param.append(Symbol(ast.conName, init_type, const_value, self.decl_num))
        

    def visitFuncDecl(self, ast, param):
        self.flag_func = self.visit(ast.retType, param)
        o = []
        for param_decl in ast.params:
            sym = self.lookup(param_decl.parName, o, lambda x: x.name)
            if sym:
                raise Redeclared(Parameter(), param_decl.parName)
            o.append(Symbol(param_decl.parName, param_decl.parType))
        self.visit(ast.body, o + param)
        self.flag_func = None
    

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
                raise TypeMismatch(ast)
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
        o = []
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
                const_value = self.cal_const(stmt.iniExpr, o + param)
                o.append(Symbol(stmt.conName, init_type, const_value))
            
            elif type(stmt) is Assign:
                lhs_type = self.visit(stmt, o + param)
                if not lhs_type:
                    self.flag_expr = 1
                    o.append(Symbol(stmt.lhs.name, self.visit(stmt.rhs, o + param)))
                    self.flag_expr = 0

            else:
                self.visit(stmt, o + param)


    def visitAssign(self, ast, param):
        self.flag_expr = 1
        rhs_type, lhs_type = self.visit(ast.rhs, param), None
        self.flag_expr = 0
        if type(ast.lhs) is not Id:
            self.flag_expr = 1
            lhs_type = self.visit(ast.lhs, param)
            self.flag_expr = 0
        else:
            res = self.lookup(ast.lhs.name, param, lambda x: x.name)
            if res and type(res.mtype) is not MType and not self.check_Type(res):
                lhs_type = self.visit(res.mtype, param) if type(res.mtype) is not MType else res.mtype
        if not self.check_type(lhs_type, rhs_type, param):
            raise TypeMismatch(ast)
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
                const_value = self.cal_const(stmt.iniExpr, o + param)
                o.append(Symbol(stmt.conName, init_type, const_value))
            
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
        tmp = self.flag_expr
        if ast.expr:
            self.flag_expr = 1
            if type(ast.expr) is not Id:
                return_type = self.visit(ast.expr, param)
            else:
                res = self.lookup(ast.expr.name, param, lambda x: x.name)
                if res and not self.check_Type(res):
                    return_type = self.visit(res.mtype, param)
                else:
                    raise Undeclared(Identifier(), ast.expr.name)
        self.flag_expr = tmp
        if self.flag_func:
            if not self.check_exact_type(return_type, self.flag_func, param):
                raise TypeMismatch(ast)


    def visitBinaryOp(self, ast, param):
        self.flag_expr = 1
        ltype = self.visit(ast.left, param)
        rtype = self.visit(ast.right, param)
        if ast.op == '+':
            if type(ltype) is IntType and type(rtype) is IntType:
                return IntType()
            elif type(ltype) is FloatType and type(rtype) is FloatType:
                return FloatType()
            elif (type(ltype) is IntType and type(rtype) is FloatType) or (type(ltype) is FloatType and type(rtype) is IntType):
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
        func_type = None
        for sym in param:
            if type(sym.mtype) is not MType:
                continue
            elif sym.name == ast.funName:
                func_type = sym
        # func_type = self.lookup(ast.funName, param, lambda x: x.name)
        if func_type is None:
            raise Undeclared(Function(), ast.funName)
        if len(ast.args) != len(func_type.mtype.partype):
            raise TypeMismatch(ast)
        tmp = self.flag_expr
        self.flag_expr = 1
        for i in range(0, len(ast.args)):
            arg_type = self.visit(ast.args[i], param)
            func_type_arg = self.visit(func_type.mtype.partype[i], param)
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
            raise TypeMismatch(ast)
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