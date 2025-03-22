# Generated from main/minigo/parser/MiniGo.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniGoParser import MiniGoParser
else:
    from MiniGoParser import MiniGoParser

# This class defines a complete generic visitor for a parse tree produced by MiniGoParser.

class MiniGoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#decl.
    def visitDecl(self, ctx:MiniGoParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#stmt.
    def visitStmt(self, ctx:MiniGoParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#block.
    def visitBlock(self, ctx:MiniGoParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#var_decl.
    def visitVar_decl(self, ctx:MiniGoParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#const_decl.
    def visitConst_decl(self, ctx:MiniGoParser.Const_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#assign_stmt.
    def visitAssign_stmt(self, ctx:MiniGoParser.Assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#lhs.
    def visitLhs(self, ctx:MiniGoParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#if_stmt.
    def visitIf_stmt(self, ctx:MiniGoParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#only_if_stmt.
    def visitOnly_if_stmt(self, ctx:MiniGoParser.Only_if_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#else_if_list.
    def visitElse_if_list(self, ctx:MiniGoParser.Else_if_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#else_stmt.
    def visitElse_stmt(self, ctx:MiniGoParser.Else_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_stmt.
    def visitFor_stmt(self, ctx:MiniGoParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#basic_for_loop.
    def visitBasic_for_loop(self, ctx:MiniGoParser.Basic_for_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_loop_initial.
    def visitFor_loop_initial(self, ctx:MiniGoParser.For_loop_initialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#initialization.
    def visitInitialization(self, ctx:MiniGoParser.InitializationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#update.
    def visitUpdate(self, ctx:MiniGoParser.UpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_loop_range.
    def visitFor_loop_range(self, ctx:MiniGoParser.For_loop_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#break_stmt.
    def visitBreak_stmt(self, ctx:MiniGoParser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#continue_stmt.
    def visitContinue_stmt(self, ctx:MiniGoParser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#call_stmt.
    def visitCall_stmt(self, ctx:MiniGoParser.Call_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#return_stmt.
    def visitReturn_stmt(self, ctx:MiniGoParser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#func_decl.
    def visitFunc_decl(self, ctx:MiniGoParser.Func_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#func_call.
    def visitFunc_call(self, ctx:MiniGoParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#argument_list.
    def visitArgument_list(self, ctx:MiniGoParser.Argument_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#method_decl.
    def visitMethod_decl(self, ctx:MiniGoParser.Method_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#method_call.
    def visitMethod_call(self, ctx:MiniGoParser.Method_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#primitive_type.
    def visitPrimitive_type(self, ctx:MiniGoParser.Primitive_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#typ.
    def visitTyp(self, ctx:MiniGoParser.TypContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr.
    def visitExpr(self, ctx:MiniGoParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr1.
    def visitExpr1(self, ctx:MiniGoParser.Expr1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr2.
    def visitExpr2(self, ctx:MiniGoParser.Expr2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr3.
    def visitExpr3(self, ctx:MiniGoParser.Expr3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr4.
    def visitExpr4(self, ctx:MiniGoParser.Expr4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr5.
    def visitExpr5(self, ctx:MiniGoParser.Expr5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expr6.
    def visitExpr6(self, ctx:MiniGoParser.Expr6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#sub_expr.
    def visitSub_expr(self, ctx:MiniGoParser.Sub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#operand.
    def visitOperand(self, ctx:MiniGoParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_type.
    def visitArray_type(self, ctx:MiniGoParser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_literal_box.
    def visitArray_literal_box(self, ctx:MiniGoParser.Array_literal_boxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_access_box.
    def visitArray_access_box(self, ctx:MiniGoParser.Array_access_boxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_literal.
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_ele_list.
    def visitArray_ele_list(self, ctx:MiniGoParser.Array_ele_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_ele.
    def visitArray_ele(self, ctx:MiniGoParser.Array_eleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#short_array_literal.
    def visitShort_array_literal(self, ctx:MiniGoParser.Short_array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_access.
    def visitArray_access(self, ctx:MiniGoParser.Array_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_decl.
    def visitStruct_decl(self, ctx:MiniGoParser.Struct_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_field.
    def visitStruct_field(self, ctx:MiniGoParser.Struct_fieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_literal.
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_ele_list.
    def visitStruct_ele_list(self, ctx:MiniGoParser.Struct_ele_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_ele.
    def visitStruct_ele(self, ctx:MiniGoParser.Struct_eleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_access.
    def visitStruct_access(self, ctx:MiniGoParser.Struct_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_array_method.
    def visitStruct_array_method(self, ctx:MiniGoParser.Struct_array_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#interface_decl.
    def visitInterface_decl(self, ctx:MiniGoParser.Interface_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#interface_method.
    def visitInterface_method(self, ctx:MiniGoParser.Interface_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#param_list.
    def visitParam_list(self, ctx:MiniGoParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#param_decl.
    def visitParam_decl(self, ctx:MiniGoParser.Param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arith_high_operator.
    def visitArith_high_operator(self, ctx:MiniGoParser.Arith_high_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arith_low_operator.
    def visitArith_low_operator(self, ctx:MiniGoParser.Arith_low_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#relational_operator.
    def visitRelational_operator(self, ctx:MiniGoParser.Relational_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#assign_operator.
    def visitAssign_operator(self, ctx:MiniGoParser.Assign_operatorContext):
        return self.visitChildren(ctx)



del MiniGoParser