from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *
from functools import reduce

class ASTGeneration(MiniGoVisitor):
    # Program
    def visitProgram(self,ctx:MiniGoParser.ProgramContext):
        return Program([self.visit(x) for x in ctx.decl()])
    
    
    # Declaration
    def visitDecl(self,ctx:MiniGoParser.DeclContext):
        return self.visit(ctx.getChild(0))
    
    
    # Statements
    def visitStmt(self,ctx:MiniGoParser.StmtContext):
        return self.visit(ctx.getChild(0))
    
    
    # Block
    def visitBlock(self,ctx:MiniGoParser.BlockContext):
        return Block([self.visit(x) for x in ctx.stmt()])
    
    	
    # Variable, Constant Declaration
    def visitVar_decl(self,ctx:MiniGoParser.Var_declContext):
        return VarDecl(ctx.IDENTIFIER().getText(),
                       self.visit(ctx.typ()) if ctx.typ() else None,
                       self.visit(ctx.expr()) if ctx.expr() else None)
    
    def visitConst_decl(self,ctx:MiniGoParser.Const_declContext):
        return ConstDecl(ctx.IDENTIFIER().getText(), None, self.visit(ctx.expr()))
    

    # Assignment Statement
    def visitAssign_stmt(self,ctx:MiniGoParser.Assign_stmtContext):
        lhs = self.visit(ctx.lhs())
        rhs = self.visit(ctx.expr())
        op = ctx.assign_operator().getText()
        if op == ':=':
            return Assign(lhs, rhs)
        else:
            return Assign(lhs, BinaryOp(op[0], lhs, rhs))
        
    def visitLhs(self,ctx:MiniGoParser.LhsContext):
        if ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            return self.visit(ctx.getChild(0))
    

    # If Statement
    def visitIf_stmt(self,ctx:MiniGoParser.If_stmtContext):
        x = self.visit(ctx.only_if_stmt())
        y = self.visit(ctx.else_if_list())[::-1] + [x]
        z = self.visit(ctx.else_stmt()) if ctx.else_stmt() else None
        return reduce(lambda acc, ele: If(ele.expr, ele.thenStmt, acc), y, z)

    def visitOnly_if_stmt(self,ctx:MiniGoParser.Only_if_stmtContext):
        return If(self.visit(ctx.expr()), self.visit(ctx.block()), None)
    
    def visitElse_if_list(self,ctx:MiniGoParser.Else_if_listContext):
        return [self.visit(x) for x in ctx.only_if_stmt()]
    
    def visitElse_stmt(self,ctx:MiniGoParser.Else_stmtContext):
        return self.visit(ctx.block())
    

    # For Statement
    def visitFor_stmt(self,ctx:MiniGoParser.For_stmtContext):
        return self.visit(ctx.getChild(0))
    
    # Basic For Loop
    def visitBasic_for_loop(self,ctx:MiniGoParser.Basic_for_loopContext):
        return ForBasic(self.visit(ctx.expr()), self.visit(ctx.block()))
    
    # For Loop with Initialization, Condition, and Update
    def visitFor_loop_initial(self,ctx:MiniGoParser.For_loop_initialContext):
        return ForStep(self.visit(ctx.initialization()), self.visit(ctx.expr()), self.visit(ctx.update()), self.visit(ctx.block()))
    
    def visitInitialization(self,ctx:MiniGoParser.InitializationContext):
        if ctx.update():
            return self.visit(ctx.update())
        else:
            return VarDecl(ctx.IDENTIFIER().getText(),
                       self.visit(ctx.typ()) if ctx.typ() else None,
                       self.visit(ctx.expr()))
    
    def visitUpdate(self,ctx:MiniGoParser.UpdateContext):
        lhs = Id(ctx.IDENTIFIER().getText())
        rhs = self.visit(ctx.expr())
        op = ctx.assign_operator().getText()
        if op == ':=':
            return Assign(lhs, rhs)
        else:
            return Assign(lhs, BinaryOp(op[0], lhs, rhs))

    # For Loop with Range
    def visitFor_loop_range(self,ctx:MiniGoParser.For_loop_rangeContext):
        return ForEach(Id(ctx.IDENTIFIER(0).getText()), Id(ctx.IDENTIFIER(1).getText()), self.visit(ctx.expr()), self.visit(ctx.block()))
    
    
    # Break Statement
    def visitBreak_stmt(self,ctx:MiniGoParser.Break_stmtContext):
        return Break()
    
    # Continue Statement
    def visitContinue_stmt(self,ctx:MiniGoParser.Continue_stmtContext):
        return Continue()
    
    # Call Statement
    def visitCall_stmt(self,ctx:MiniGoParser.Call_stmtContext):
        return self.visit(ctx.getChild(0))
    
    # Return Statement
    def visitReturn_stmt(self,ctx:MiniGoParser.Return_stmtContext):
        return Return(self.visit(ctx.expr()) if ctx.expr() else None)
    

    # Function
    # Function Declaration
    def visitFunc_decl(self,ctx:MiniGoParser.Func_declContext):
        return FuncDecl(ctx.IDENTIFIER().getText(),
                        self.visit(ctx.param_list()) if ctx.param_list() else [],
                        self.visit(ctx.typ()) if ctx.typ() else VoidType(),
                        self.visit(ctx.block()))
    
    # Function Call
    def visitFunc_call(self,ctx:MiniGoParser.Func_callContext):
        return FuncCall(ctx.IDENTIFIER().getText(), self.visit(ctx.argument_list()) if ctx.argument_list() else [])
    
    def visitArgument_list(self,ctx:MiniGoParser.Argument_listContext):
        return [self.visit(x) for x in ctx.expr()]
    

    # Method
    # Method Declaration
    def visitMethod_decl(self,ctx:MiniGoParser.Method_declContext):
        funcDecl = FuncDecl(ctx.IDENTIFIER(2).getText(),
                        self.visit(ctx.param_list()) if ctx.param_list() else [],
                        self.visit(ctx.typ()) if ctx.typ() else VoidType(),
                        self.visit(ctx.block()))
        return MethodDecl(ctx.IDENTIFIER(0).getText(), Id(ctx.IDENTIFIER(1).getText()), funcDecl)
    
    # Method Call
    def visitMethod_call(self,ctx:MiniGoParser.Method_callContext):
        funcCall = self.visit(ctx.func_call())
        return MethCall(self.visit(ctx.struct_array_method()), funcCall.funName, funcCall.args)
    

    # Type
    def visitPrimitive_type(self,ctx:MiniGoParser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():    
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return BoolType()
        
    def visitTyp(self,ctx:MiniGoParser.TypContext):
        if ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            return self.visit(ctx.getChild(0))
    

    # Expression
    def visitExpr(self,ctx:MiniGoParser.ExprContext):
        return BinaryOp(ctx.OR().getText(), self.visit(ctx.expr()), self.visit(ctx.expr1())) if ctx.OR() else self.visit(ctx.expr1())
    
    def visitExpr1(self,ctx:MiniGoParser.ExprContext):
        return BinaryOp(ctx.AND().getText(), self.visit(ctx.expr1()), self.visit(ctx.expr2())) if ctx.AND() else self.visit(ctx.expr2())
    
    def visitExpr2(self,ctx:MiniGoParser.ExprContext):
        return BinaryOp(ctx.relational_operator().getText(), self.visit(ctx.expr2()), self.visit(ctx.expr3())) if ctx.relational_operator() else self.visit(ctx.expr3())
    
    def visitExpr3(self,ctx:MiniGoParser.ExprContext):
        return BinaryOp(ctx.arith_low_operator().getText(), self.visit(ctx.expr3()), self.visit(ctx.expr4())) if ctx.arith_low_operator() else self.visit(ctx.expr4())
    
    def visitExpr4(self,ctx:MiniGoParser.ExprContext):
        return BinaryOp(ctx.arith_high_operator().getText(), self.visit(ctx.expr4()), self.visit(ctx.expr5())) if ctx.arith_high_operator() else self.visit(ctx.expr5())
    
    def visitExpr5(self,ctx:MiniGoParser.ExprContext):
        return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.expr5())) if ctx.expr5() else self.visit(ctx.expr6())
    
    def visitExpr6(self,ctx:MiniGoParser.ExprContext):
        return self.visit(ctx.getChild(0))
    
    # Sub-Expression
    def visitSub_expr(self,ctx:MiniGoParser.Sub_exprContext):
        return self.visit(ctx.expr())
    

    # Operand
    def visitOperand(self,ctx:MiniGoParser.OperandContext):
        if ctx.INTEGER_LITERAL():
            return IntLiteral(ctx.INTEGER_LITERAL().getText())
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(ctx.FLOAT_LITERAL().getText())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.BOOLEAN_LITERAL():
            return BooleanLiteral(ctx.BOOLEAN_LITERAL().getText() == 'true')
        elif ctx.NIL_LITERAL():
            return NilLiteral()
        elif ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            return self.visit(ctx.getChild(0))


    # Array
    # Array Type
    def visitArray_type(self,ctx:MiniGoParser.Array_typeContext):
        if ctx.array_type():
            return ArrayType([self.visitArray_literal_box(ctx.array_literal_box())] + self.visit(ctx.array_type()).dimens, self.visit(ctx.array_type()).eleType)
        else:
            return ArrayType([self.visit(ctx.array_literal_box())], self.visit(ctx.primitive_type()) if ctx.primitive_type() else Id(ctx.IDENTIFIER().getText()))
        
    def visitArray_literal_box(self,ctx:MiniGoParser.Array_literal_boxContext):
        return IntLiteral(ctx.INTEGER_LITERAL().getText()) if ctx.INTEGER_LITERAL() else Id(ctx.IDENTIFIER().getText())
    
    def visitArray_access_box(self,ctx:MiniGoParser.Array_access_boxContext):
        return self.visit(ctx.expr())
    
    # Array Literal
    def visitArray_literal(self,ctx:MiniGoParser.Array_literalContext):
        return ArrayLiteral(self.visit(ctx.array_type()).dimens, self.visit(ctx.array_type()).eleType, self.visit(ctx.array_ele_list()))
    
    def visitArray_ele_list(self,ctx:MiniGoParser.Array_ele_listContext):
        return [self.visit(x) for x in ctx.array_ele()]
        
    def visitArray_ele(self,ctx:MiniGoParser.Array_eleContext):
        if ctx.INTEGER_LITERAL():
            return IntLiteral(ctx.INTEGER_LITERAL().getText())
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(ctx.FLOAT_LITERAL().getText())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.BOOLEAN_LITERAL():
            return BooleanLiteral(ctx.BOOLEAN_LITERAL().getText() == 'true')
        elif ctx.NIL_LITERAL():
            return NilLiteral()
        elif ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            return self.visit(ctx.getChild(0))
        
    def visitShort_array_literal(self,ctx:MiniGoParser.Short_array_literalContext):
        return ArrayLiteral([], VoidType(), self.visit(ctx.array_ele_list()))
    
    # Array Access
    def visitArray_access(self,ctx:MiniGoParser.Array_accessContext):
        if ctx.operand():
            return ArrayCell(self.visit(ctx.operand()), [self.visit(x) for x in ctx.array_access_box()])
        elif ctx.IDENTIFIER():
            return ArrayCell(FieldAccess(self.visit(ctx.struct_array_method()), ctx.IDENTIFIER().getText()), [self.visit(x) for x in ctx.array_access_box()])
        else:
            funcCall = self.visit(ctx.func_call())
            return ArrayCell(MethCall(self.visit(ctx.struct_array_method()), funcCall.funName, funcCall.args), [self.visit(x) for x in ctx.array_access_box()])


    # Struct
    # Struct Declaration
    def visitStruct_decl(self,ctx:MiniGoParser.Struct_declContext):
        return StructType(ctx.IDENTIFIER().getText(), [self.visit(x) for x in ctx.struct_field()], [])
    
    def visitStruct_field(self,ctx:MiniGoParser.Struct_fieldContext):
        return (ctx.IDENTIFIER().getText(), self.visit(ctx.typ()))
    
    # Struct Literal
    def visitStruct_literal(self,ctx:MiniGoParser.Struct_literalContext):
        return StructLiteral(ctx.IDENTIFIER().getText(), self.visit(ctx.struct_ele_list()) if ctx.struct_ele_list() else [])
    
    def visitStruct_ele_list(self,ctx:MiniGoParser.Struct_ele_listContext):
        return [self.visit(x) for x in ctx.struct_ele()]
    
    def visitStruct_ele(self,ctx:MiniGoParser.Struct_eleContext):
        return (ctx.IDENTIFIER().getText(), self.visit(ctx.expr()))
    
    # Struct Access
    def visitStruct_access(self,ctx:MiniGoParser.Struct_accessContext):
        return FieldAccess(self.visit(ctx.struct_array_method()), ctx.IDENTIFIER().getText())
    
    # Struct Array Method joint
    def visitStruct_array_method(self,ctx:MiniGoParser.Struct_array_methodContext):
        if ctx.operand():
            return self.visit(ctx.operand())
        elif ctx.IDENTIFIER():
            return FieldAccess(self.visit(ctx.struct_array_method()), ctx.IDENTIFIER().getText())
        elif ctx.array_access_box():
            return ArrayCell(self.visit(ctx.struct_array_method()), [self.visit(x) for x in ctx.array_access_box()])
        else:
            return MethCall(self.visit(ctx.struct_array_method()), self.visit(ctx.func_call()).funName, self.visit(ctx.func_call()).args)
    
    # Interface
    # Interface Declaration
    def visitInterface_decl(self,ctx:MiniGoParser.Interface_declContext):
        return InterfaceType(ctx.IDENTIFIER().getText(), [self.visit(x) for x in ctx.interface_method()])
    
    def visitInterface_method(self,ctx:MiniGoParser.Interface_methodContext):
        paramList = self.visit(ctx.param_list()) if ctx.param_list() else []
        paramTypeList = [x.parType for x in paramList]
        return Prototype(ctx.IDENTIFIER().getText(), paramTypeList, self.visit(ctx.typ()) if ctx.typ() else VoidType())
    
    def visitParam_list(self,ctx:MiniGoParser.Param_listContext):
        return reduce(lambda acc, ele: acc + ele, [self.visit(x) for x in ctx.param_decl()], [])
    
    def visitParam_decl(self,ctx:MiniGoParser.Param_declContext):
        return [ParamDecl(x.getText(), self.visit(ctx.typ())) for x in ctx.IDENTIFIER()]
    
    
    # Operators    
    def visitArith_high_operator(self,ctx:MiniGoParser.Arith_high_operatorContext):   
        return ctx.getChild(0).getText()
    
    def visitArith_low_operator(self,ctx:MiniGoParser.Arith_low_operatorContext):
        return ctx.getChild(0).getText()
    
    def visitRelational_operator(self,ctx:MiniGoParser.Relational_operatorContext):
        return ctx.getChild(0).getText()
    
    def visitAssign_operator(self,ctx:MiniGoParser.Assign_operatorContext):
        return ctx.getChild(0).getText()