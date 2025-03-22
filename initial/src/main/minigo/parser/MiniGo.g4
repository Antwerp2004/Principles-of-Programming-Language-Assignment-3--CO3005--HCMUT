// Student's ID: 2212779

grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
def __init__(self, input:InputStream):
    super().__init__(input)
    self.checkVersion("4.9.2")
    self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
    self._actions = None
    self._predicates = None
    self.preType = None

def emit(self):
    tk = self.type
    result = super().emit()
    self.preType = tk
    return result
}

options{
	language = Python3;
}

// Program
program  : decl+ EOF ;

// Declaration
decl: var_decl | const_decl
    | struct_decl | interface_decl
    | func_decl | method_decl ;

// Statements
stmt: var_decl | const_decl
    | assign_stmt
    | if_stmt
    | for_stmt
    | break_stmt | continue_stmt
    | call_stmt | return_stmt ;
// Block
block: OPEN_BRACE stmt+ CLOSE_BRACE;

// Variable, Constant Declaration
var_decl: VAR IDENTIFIER (typ | EQUAL expr | typ EQUAL expr) SEMICOLON;
const_decl: CONST IDENTIFIER EQUAL expr SEMICOLON;

// Assignment Statement
assign_stmt: lhs assign_operator expr SEMICOLON;
lhs: IDENTIFIER | struct_access | array_access;

// If Statement
if_stmt: only_if_stmt else_if_list else_stmt? SEMICOLON;
only_if_stmt: IF OPEN_PARENTHESIS expr CLOSE_PARENTHESIS block;
else_if_list: (ELSE only_if_stmt)*;
else_stmt: ELSE block;

// For Statement
for_stmt: basic_for_loop | for_loop_initial | for_loop_range;
// Basic For Loop
basic_for_loop: FOR expr block SEMICOLON;
// For Loop with Initialization, Condition, and Update
for_loop_initial: FOR initialization expr SEMICOLON update block SEMICOLON;
initialization: update SEMICOLON 
              | VAR IDENTIFIER (EQUAL expr | typ EQUAL expr) SEMICOLON;
update: IDENTIFIER assign_operator expr;
// For Loop with Range
for_loop_range: FOR IDENTIFIER COMMA IDENTIFIER ASSIGNMENT_SIGN RANGE expr block SEMICOLON;

// Break Statement
break_stmt: BREAK SEMICOLON;
// Continue Statement
continue_stmt: CONTINUE SEMICOLON;

// Call Statement
call_stmt: (func_call | method_call) SEMICOLON;
// Return Statement
return_stmt: RETURN expr? SEMICOLON;


// Function
// Function Declaration
func_decl: FUNC IDENTIFIER OPEN_PARENTHESIS param_list? CLOSE_PARENTHESIS typ? block SEMICOLON;
// Function Call
func_call: IDENTIFIER OPEN_PARENTHESIS argument_list? CLOSE_PARENTHESIS;
argument_list: expr (COMMA expr)*;


// Method
// Method Declaration
method_decl: FUNC OPEN_PARENTHESIS IDENTIFIER IDENTIFIER CLOSE_PARENTHESIS 
        IDENTIFIER OPEN_PARENTHESIS param_list? CLOSE_PARENTHESIS typ? block SEMICOLON;
// Method Call
method_call: struct_array_method DOT func_call;


// Type
primitive_type: INT | FLOAT | STRING | BOOLEAN;
typ: primitive_type | IDENTIFIER | array_type;


// Expression
expr: expr OR expr1 | expr1;
expr1: expr1 AND expr2 | expr2;
expr2: expr2 relational_operator expr3 | expr3;
expr3: expr3 arith_low_operator expr4 | expr4;
expr4: expr4 arith_high_operator expr5 | expr5;
expr5: (NOT | SUB) expr5 | expr6;
expr6: struct_access | array_access | method_call | operand;
// Sub-Expression
sub_expr: OPEN_PARENTHESIS expr CLOSE_PARENTHESIS;


// Operand
operand:  INTEGER_LITERAL
        | FLOAT_LITERAL
        | STRING_LITERAL
        | BOOLEAN_LITERAL
        | NIL_LITERAL
        | array_literal
        | struct_literal
        | IDENTIFIER
        | func_call
        | sub_expr;


// Array
// Array Type
array_type: array_literal_box array_type | array_literal_box (primitive_type | IDENTIFIER);
array_literal_box: OPEN_BRACKET (INTEGER_LITERAL | IDENTIFIER) CLOSE_BRACKET;
array_access_box: OPEN_BRACKET expr CLOSE_BRACKET;

// Array Literal
array_literal: array_type OPEN_BRACE array_ele_list CLOSE_BRACE;
array_ele_list: array_ele (COMMA array_ele)*;
array_ele: INTEGER_LITERAL | FLOAT_LITERAL | BOOLEAN_LITERAL | STRING_LITERAL | NIL_LITERAL
         | IDENTIFIER | struct_literal | short_array_literal;
short_array_literal: OPEN_BRACE array_ele_list CLOSE_BRACE;
// Array Access
array_access: struct_array_method (DOT IDENTIFIER | DOT func_call) array_access_box+ | operand array_access_box+;


// Struct
// Struct Declaration
struct_decl: TYPE IDENTIFIER STRUCT OPEN_BRACE struct_field+ CLOSE_BRACE SEMICOLON;
struct_field: IDENTIFIER typ SEMICOLON;

// Struct Literal
struct_literal: IDENTIFIER OPEN_BRACE struct_ele_list? CLOSE_BRACE;
struct_ele_list: struct_ele (COMMA struct_ele)*;
struct_ele: IDENTIFIER COLON expr;
// Struct Access
struct_access: struct_array_method DOT IDENTIFIER;

// Struct Array Method joint
struct_array_method: operand | struct_array_method DOT IDENTIFIER | struct_array_method array_access_box+ | struct_array_method DOT func_call;


// Interface
// Interface Declaration
interface_decl: TYPE IDENTIFIER INTERFACE OPEN_BRACE interface_method+ CLOSE_BRACE SEMICOLON;
interface_method: IDENTIFIER OPEN_PARENTHESIS param_list? CLOSE_PARENTHESIS typ? SEMICOLON;
param_list: param_decl (COMMA param_decl)*;
param_decl: IDENTIFIER (COMMA IDENTIFIER)* typ;


// Operators
arith_high_operator: MULTIPLY | DIVIDE | REMAIN;
arith_low_operator: ADD | SUB;
relational_operator: COMPARE_STR | NOT_EQ | GREATER_OR_EQ | LESS_OR_EQ | GREATER | LESS;
assign_operator: ASSIGNMENT_SIGN | SHORT_ADD | SHORT_SUB | SHORT_MULTIPLY | SHORT_DIVIDE | SHORT_REMAIN;


// Comments
// Single-line Comments
SINGLE_LINE_COMMENT: '//' (~[\r\n])* -> skip;
// Multi-line Comments
MULTI_LINE_COMMENT: '/*' (MULTI_LINE_COMMENT|.)*? '*/' -> skip;


// Keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';


// Operators
// Arithmetic
ADD: '+';
SUB: '-';
MULTIPLY: '*';
DIVIDE: '/';
REMAIN: '%';

// Relational
COMPARE_STR: '==';
NOT_EQ: '!=';
GREATER_OR_EQ: '>=';
LESS_OR_EQ: '<=';
GREATER: '>';
LESS: '<';

// Logical
AND: '&&';
OR: '||';
NOT: '!';

// Assignment
ASSIGNMENT_SIGN: ':=';
SHORT_ADD: '+=';
SHORT_SUB: '-=';
SHORT_MULTIPLY: '*=';
SHORT_DIVIDE: '/=';
SHORT_REMAIN: '%=';

// Other
EQUAL: '=';
DOT: '.';


// Separators
OPEN_PARENTHESIS: '(';
CLOSE_PARENTHESIS: ')';
OPEN_BRACKET: '[';
CLOSE_BRACKET: ']';
OPEN_BRACE: '{';
CLOSE_BRACE: '}';
COMMA: ',';
SEMICOLON: ';';
COLON: ':';


// Literals
// Integer Literals
INTEGER_LITERAL: DECIMAL_INT | BINARY_INT | OCTAL_INT | HEXA_INT;
DECIMAL_INT: '0' | [1-9] [0-9]*;
BINARY_INT: '0' [bB] [01]+;
OCTAL_INT: '0' [oO] [0-7]+;
HEXA_INT: '0' [xX] [0-9a-fA-F]+;

// Floating-point Literals
FLOAT_LITERAL: INT_PART '.' DECI_PART? EXP_PART?;
fragment INT_PART: [0-9]+;
fragment DECI_PART: [0-9]*;
fragment EXP_PART: [eE] [+-]? [0-9]+;

// String Literals
STRING_LITERAL: (DOUBLE_QUOTE DOUBLE_QUOTE | DOUBLE_QUOTE INSIDE_STRING+ DOUBLE_QUOTE);// {self.text = self.text[1:-1]};
fragment INSIDE_STRING: ESCAPE_SEQUENCE | ~[\n\r"\\];
fragment DOUBLE_QUOTE: ["];
fragment BACKLASH: '\\';
fragment ESCAPE_SEQUENCE: (BACKLASH [ntr]) | (BACKLASH DOUBLE_QUOTE) | (BACKLASH BACKLASH);

// Boolean Literals
BOOLEAN_LITERAL: 'true' | 'false';
// Nil Literal
NIL_LITERAL: 'nil';


NEWLINE: ('\r\n' | '\n')
         {
            if self.preType in {self.IDENTIFIER, self.INTEGER_LITERAL,
            self.FLOAT_LITERAL, self.BOOLEAN_LITERAL, self.STRING_LITERAL,
            self.INT, self.FLOAT, self.BOOLEAN, self.STRING,
            self.RETURN, self.CONTINUE, self.BREAK, self.NIL_LITERAL,
            self.CLOSE_PARENTHESIS, self.CLOSE_BRACKET, self.CLOSE_BRACE}:
                self.text = ";"
                self.type = self.SEMICOLON
            else:
                self.skip()
         };


// Whitespace
WHITESPACE: [ \t\f\r] -> skip;

// Identifiers
IDENTIFIER: [A-Za-z_] [A-Za-z_0-9]*;


ILLEGAL_ESCAPE: DOUBLE_QUOTE INSIDE_STRING* BACKLASH ~[ntr\\] {raise IllegalEscape(self.text)};
UNCLOSE_STRING: DOUBLE_QUOTE INSIDE_STRING* ([\r\n] | EOF) 
                {
                    if self.text[-1] in ['\r', '\n']:
                        raise UncloseString(self.text[:-1])
                    else:
                        raise UncloseString(self.text)
                };
ERROR_CHAR: . {raise ErrorToken(self.text)};