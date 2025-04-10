import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    ASTGenTest = 299
    
#     def test_ASTGen_00(self):
#         inp = \
#             """
# type S1 struct {votien int;}
# type I1 interface {votien();}
# var a I1;
# var c I1;
# var d S1;
# func foo(){
#     c := a;
#     d := S1{votien:8};
# }

# var e int = 6.0;
#         """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,IntLiteral(5)),VarDecl(y,IntType,IntLiteral(10)),VarDecl(result,IntType,BinaryOp(Id(x),+,BinaryOp(Id(y),*,IntLiteral(2)))),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_01(self):
#         inp = \
#             """// Test case 1: String manipulation and conditional output
# func main() {
#     var name string = "MiniGo";
#     var greeting string = "Hello, " + name + "!";
#     if (len(greeting) > 10) {
#         println(greeting)
#     }
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(name,StringType,StringLiteral("MiniGo")),VarDecl(greeting,StringType,BinaryOp(BinaryOp(StringLiteral("Hello, "),+,Id(name)),+,StringLiteral("!"))),If(BinaryOp(FuncCall(len,[Id(greeting)]),>,IntLiteral(10)),Block([FuncCall(println,[Id(greeting)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_02(self):
#         inp = \
#             """// Test case 2: Function with parameters, local variables, and return
# func add(a int, b int) int {
#     var sum int = a + b;
#     return sum
# }
# func main() {
#     var result int = add(5, 3);
#     println(result);
# }
# """
#         out = """Program([FuncDecl(add,[ParDecl(a,IntType),ParDecl(b,IntType)],IntType,Block([VarDecl(sum,IntType,BinaryOp(Id(a),+,Id(b))),Return(Id(sum))])),FuncDecl(main,[],VoidType,Block([VarDecl(result,IntType,FuncCall(add,[IntLiteral(5),IntLiteral(3)])),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_03(self):
#         inp = \
#             """const VT = [1]ID{1, 3};"""
#         out = """Program([ConstDecl(VT,ArrayLiteral([IntLiteral(1)],Id(ID),[IntLiteral(1),IntLiteral(3)]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_04(self):
#         inp = \
#             """/* Test case 4: Array declaration, initialization, and iteration*/
# func main() {
#     var numbers [abc]int = [6]float{1, 2, 3, 4, 5}
#     var sum int = 0
#     for i := 0; i < 5; i += 1 {
#         sum := sum + numbers[i];
#     }
#     println(sum)
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(numbers,ArrayType(IntType,[Id(abc)]),ArrayLiteral([IntLiteral(6)],FloatType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5)])),VarDecl(sum,IntType,IntLiteral(0)),For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(5)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([Assign(Id(sum),BinaryOp(Id(sum),+,ArrayCell(Id(numbers),[Id(i)])))])),FuncCall(println,[Id(sum)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_05(self):
#         inp = \
#             """// Test case 5: Nested if statements with logical operators
# func main() {
#     var age int = 25;
#     var isStudent boolean = true;
#     if (age > 18 && age < 30) {
#         if (isStudent) {
#             println("Eligible for student discount");
#         } else {
#             println("Eligible for adult fare");
#         }
#     } else {
#         println("Not eligible");
#     }
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(age,IntType,IntLiteral(25)),VarDecl(isStudent,BoolType,BooleanLiteral(true)),If(BinaryOp(BinaryOp(Id(age),>,IntLiteral(18)),&&,BinaryOp(Id(age),<,IntLiteral(30))),Block([If(Id(isStudent),Block([FuncCall(println,[StringLiteral("Eligible for student discount")])]),Block([FuncCall(println,[StringLiteral("Eligible for adult fare")])]))]),Block([FuncCall(println,[StringLiteral("Not eligible")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_06(self):
#         inp = \
#             """
# // Test case 6: For loop with break and continue statements
# func main() {
#     for i := 0; i < 10; i += 1 {
#         if (i % 2 == 0) {
#             continue;
#         }
#         if (i > 5) {
#             break;
#         }
#         println(i);
#     }
#     println("Loop finished");
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(i),%,IntLiteral(2)),==,IntLiteral(0)),Block([Continue()])),If(BinaryOp(Id(i),>,IntLiteral(5)),Block([Break()])),FuncCall(println,[Id(i)])])),FuncCall(println,[StringLiteral("Loop finished")])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_07(self):
#         inp = \
#             """// Test case 7: Multiple function calls with different parameters
# func square(x int) int {
#     return x * x;
# }
# func cube(x int) int {
#     return x * x * x;
# }
# func main() {
#     var sq int = square(5);
#     var cb int = cube(3);
#     println(sq)
#     println(cb)
# }
# """
#         out = """Program([FuncDecl(square,[ParDecl(x,IntType)],IntType,Block([Return(BinaryOp(Id(x),*,Id(x)))])),FuncDecl(cube,[ParDecl(x,IntType)],IntType,Block([Return(BinaryOp(BinaryOp(Id(x),*,Id(x)),*,Id(x)))])),FuncDecl(main,[],VoidType,Block([VarDecl(sq,IntType,FuncCall(square,[IntLiteral(5)])),VarDecl(cb,IntType,FuncCall(cube,[IntLiteral(3)])),FuncCall(println,[Id(sq)]),FuncCall(println,[Id(cb)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_08(self):
#         inp = \
#             """// Test case 8: Interface definition and empty implementation
# type Printable interface {
#     print();
# }
# type Empty struct {a Triangle;}
# func (e Empty) print() {a := b;}
# func main() {
#     var p Printable = Empty{};
#     p.print();
# }
# """
#         out = """Program([InterfaceType(Printable,[Prototype(print,[],VoidType)]),StructType(Empty,[(a,Id(Triangle))],[]),MethodDecl(e,Id(Empty),FuncDecl(print,[],VoidType,Block([Assign(Id(a),Id(b))]))),FuncDecl(main,[],VoidType,Block([VarDecl(p,Id(Printable),StructLiteral(Empty,[])),MethodCall(Id(p),print,[])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_09(self):
#         inp = \
#             """// Test case 9: Function with multiple local variables and complex calculations
# func calculate(a int, b,c int, c float) int {
#     var x int = a + b;
#     var y int = b * c
#     var z int = x - y
#     return z * 2;
# }
# func main() {
#     var result int = calculate(10, 5, 2);
#     println(result);
# }
# """
#         out = """Program([FuncDecl(calculate,[ParDecl(a,IntType),ParDecl(b,IntType),ParDecl(c,IntType),ParDecl(c,FloatType)],IntType,Block([VarDecl(x,IntType,BinaryOp(Id(a),+,Id(b))),VarDecl(y,IntType,BinaryOp(Id(b),*,Id(c))),VarDecl(z,IntType,BinaryOp(Id(x),-,Id(y))),Return(BinaryOp(Id(z),*,IntLiteral(2)))])),FuncDecl(main,[],VoidType,Block([VarDecl(result,IntType,FuncCall(calculate,[IntLiteral(10),IntLiteral(5),IntLiteral(2)])),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_10(self):
#         inp = \
#             """// Test case 10: Error: Missing semicolon
# func main() { var x int = 5 ;}
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,IntLiteral(5))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_11(self):
#         inp = \
#             """// Test case 11: Error: Unclosed parenthesis
# func main() { if (true +  [2]int{1,2}) {a:=b;};}
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([If(BinaryOp(BooleanLiteral(true),+,ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)])),Block([Assign(Id(a),Id(b))]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_12(self):
#         inp = \
#             """// Test case 12: Error: Undeclared variable
# func main() { x -= 5; }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([Assign(Id(x),BinaryOp(Id(x),-,IntLiteral(5)))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_13(self):
#         inp = \
#             """// Test case 13: Error: Type mismatch
# func main() { var x int = "hello"; }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,StringLiteral("hello"))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_14(self):
#         inp = \
#             """// Test case 14: Error: Invalid operator
# func main() { var x int = 5 / 3; }"""
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,BinaryOp(IntLiteral(5),/,IntLiteral(3)))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_15(self):
#         inp = \
#             """
#             type Calculator interface {
                                        
#                 Add(x, y int) int;
#                 Subtract(a, b float, c int) [3]ID;
#                 Reset()
                                        
#                 SayHello(name string);
                                        
#             }
#             type VT interface {Add(x, y int) int;}                                                                       
#         """
#         out = """Program([InterfaceType(Calculator,[Prototype(Add,[IntType,IntType],IntType),Prototype(Subtract,[FloatType,FloatType,IntType],ArrayType(Id(ID),[IntLiteral(3)])),Prototype(Reset,[],VoidType),Prototype(SayHello,[StringType],VoidType)]),InterfaceType(VT,[Prototype(Add,[IntType,IntType],IntType)])])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_16(self):
#         inp = \
#             """// Test case 16: Error: Invalid return type
# func foo() int { return "hello"; }
# func main() {Add(x, y);}
# """
#         out = """Program([FuncDecl(foo,[],IntType,Block([Return(StringLiteral("hello"))])),FuncDecl(main,[],VoidType,Block([FuncCall(Add,[Id(x),Id(y)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_17(self):
#         inp = \
#             """// Test case 17: Error: Array index out of bounds (for completeness - may not be a parsing error)
# func main() { var arr [3]int = [4]string{1, 2, 3}; var x int = arr[5]; }
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(arr,ArrayType(IntType,[IntLiteral(3)]),ArrayLiteral([IntLiteral(4)],StringType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])),VarDecl(x,IntType,ArrayCell(Id(arr),[IntLiteral(5)]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_18(self):
#         inp = \
#             """// Test case 18: Error: Struct field does not exist
# type Point struct { x int; }
# func main() { var p Point = Point{x: 1, y: 2}; var z int = p.z; }
# """
#         out = "Program([StructType(Point,[(x,IntType)],[]),FuncDecl(main,[],VoidType,Block([VarDecl(p,Id(Point),StructLiteral(Point,[(x,IntLiteral(1)),(y,IntLiteral(2))])),VarDecl(z,IntType,FieldAccess(Id(p),z))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_19(self):
#         inp = \
#             """
# // Test case 19: Error: Invalid character
# func main() { var x int = 50; }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,IntLiteral(50))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_20(self):
#         inp = \
#             """    
#             func VT() {                           
#                 for i < 10 {break;}
#                 break;
#                 continue;
#                 return 1;
#                 return
#                 foo(2 + x, 4 / y); m.goo();                        
#              }
                                        
#         """
#         out = """Program([FuncDecl(VT,[],VoidType,Block([For(BinaryOp(Id(i),<,IntLiteral(10)),Block([Break()])),Break(),Continue(),Return(IntLiteral(1)),Return(),FuncCall(foo,[BinaryOp(IntLiteral(2),+,Id(x)),BinaryOp(IntLiteral(4),/,Id(y))]),MethodCall(Id(m),goo,[])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_21(self):
#         inp = \
#             """// Test case 21: Multi-dimensional array
# func main() {
#     var matrix [2][1]int = [2][1]int{{1, 2, 3}, 4};
#     println(matrix[1][2]); // Output: 6
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(matrix,ArrayType(IntType,[IntLiteral(2),IntLiteral(1)]),ArrayLiteral([IntLiteral(2),IntLiteral(1)],IntType,[ArrayLiteral([],VoidType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),IntLiteral(4)])),FuncCall(println,[ArrayCell(Id(matrix),[IntLiteral(1),IntLiteral(2)])])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_22(self):
#         inp = \
#             """// Test case 22: Multiple struct instances
# type Rectangle struct {
#     width int;
#     height int;
# }
# func main() {
#     var rect1 Rectangle = Rectangle{width: 10, height: 5};
#     var rect2 Rectangle = Rectangle{width: 7, height: 3};
#     println(rect1.width * rect1.height + rect2.width * rect2.height);
# }
# """
#         out = "Program([StructType(Rectangle,[(width,IntType),(height,IntType)],[]),FuncDecl(main,[],VoidType,Block([VarDecl(rect1,Id(Rectangle),StructLiteral(Rectangle,[(width,IntLiteral(10)),(height,IntLiteral(5))])),VarDecl(rect2,Id(Rectangle),StructLiteral(Rectangle,[(width,IntLiteral(7)),(height,IntLiteral(3))])),FuncCall(println,[BinaryOp(BinaryOp(FieldAccess(Id(rect1),width),*,FieldAccess(Id(rect1),height)),+,BinaryOp(FieldAccess(Id(rect2),width),*,FieldAccess(Id(rect2),height)))])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_23(self):
#         inp = \
#             """// Test case 23: More complex function with nested loops
# func processArray(arr [5]int) int {
#     var sum int = 0;
#     for i := 0; i < 5; i += 1 {
#         for j := 0; j < arr[i]; j += 1 {
#             sum := sum + 1;
#         }
#     }
#     return sum;
# }
# func main() {
#     var data [5]int = [5]int{1, 2, 3, 4, 5};
#     var result int = processArray(data);
#     println(result); // Output: 15
# }
# """
#         out = """Program([FuncDecl(processArray,[ParDecl(arr,ArrayType(IntType,[IntLiteral(5)]))],IntType,Block([VarDecl(sum,IntType,IntLiteral(0)),For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(5)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([For(Assign(Id(j),IntLiteral(0)),BinaryOp(Id(j),<,ArrayCell(Id(arr),[Id(i)])),Assign(Id(j),BinaryOp(Id(j),+,IntLiteral(1))),Block([Assign(Id(sum),BinaryOp(Id(sum),+,IntLiteral(1)))]))])),Return(Id(sum))])),FuncDecl(main,[],VoidType,Block([VarDecl(data,ArrayType(IntType,[IntLiteral(5)]),ArrayLiteral([IntLiteral(5)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5)])),VarDecl(result,IntType,FuncCall(processArray,[Id(data)])),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_24(self):
#         inp = \
#             """ 
# // Test case 24: Method call on struct
# type Circle struct {
#     radius int;
# }
# func (c Circle) area() int {
#     return 3 * c.radius * c.radius;
# }
# func main() {
#     var myCircle Circle = Circle{radius: 5};
#     println(myCircle.area()); // Output: 75
# }
# """
#         out = """Program([StructType(Circle,[(radius,IntType)],[]),MethodDecl(c,Id(Circle),FuncDecl(area,[],IntType,Block([Return(BinaryOp(BinaryOp(IntLiteral(3),*,FieldAccess(Id(c),radius)),*,FieldAccess(Id(c),radius)))]))),FuncDecl(main,[],VoidType,Block([VarDecl(myCircle,Id(Circle),StructLiteral(Circle,[(radius,IntLiteral(5))])),FuncCall(println,[MethodCall(Id(myCircle),area,[])])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_25(self):
#         inp = \
#             """ 
# // Test case 25: Nested comments (valid)
# func main() {
#     /*
#     Outer comment
#     /* Inner comment */
#     */
#     println("Hello");
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([FuncCall(println,[StringLiteral("Hello")])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_26(self):
#         inp = \
#             """// Test case 26: Multi-line string
# func main() {
#     var message string = "This is a very long string" +
#                            "that spans multiple lines.";
#     println(message);
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(message,StringType,BinaryOp(StringLiteral("This is a very long string"),+,StringLiteral("that spans multiple lines."))),FuncCall(println,[Id(message)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_27(self):
#         inp = \
#             """ 
# // Test case 27: Global and local variable shadowing
# var globalVar int = 10;
# func main() {
#     var globalVar int = 20; // Shadows the global variable within main
#     println(globalVar);         // Output: 20
#     func inner() {
#         var globalVar int = 30; // Shadows in an inner block
#         println(globalVar);     // Output: 30
#     }
#     println(globalVar);         // Output: 20 (back to the outer main scope)
# }
# """
#         out = "Program([VarDecl(globalVar,IntType,IntLiteral(10)),FuncDecl(main,[],VoidType,Block([VarDecl(globalVar,IntType,IntLiteral(20)),FuncCall(println,[Id(globalVar)])])),FuncDecl(inner,[],VoidType,Block([VarDecl(globalVar,IntType,IntLiteral(30)),FuncCall(println,[Id(globalVar)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_28(self):
#         inp = \
#             """ // Test case 28: Nil pointer check and usage (check if ASTGen allows nil)
# func main() {
#     var ptr = nil;
#     if (ptr == nil) {
#         println("Pointer is nil");
#     }
#     // The following line might cause a runtime error if nil pointers aren't handled
#     // println(*ptr);  // Remove or comment out for ASTGen testing, address in later stages.
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(ptr,Nil),If(BinaryOp(Id(ptr),==,Nil),Block([FuncCall(println,[StringLiteral("Pointer is nil")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_29(self):
#         inp = \
#             """ // Test case 29: Test for "range" with a single value
# func main() {
# 	arr := [3]int{1,2,3}
# 	for _, value := range arr {
# 		println(value)
# 	}
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([Assign(Id(arr),ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])),ForEach(Id(_),Id(value),Id(arr),Block([FuncCall(println,[Id(value)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_30(self):
#         inp = \
#             """ 
# // Test case 30:  Use Struct and function calls within a statement.
# type example_t struct {
# 	x int
# }
# func calc(e example_t) int{
# 	return e.x + 10
# }
# func main() {
# 	var e example_t = example_t{x: 10}

# 	println(calc(e))
# }
# """
#         out = "Program([StructType(example_t,[(x,IntType)],[]),FuncDecl(calc,[ParDecl(e,Id(example_t))],IntType,Block([Return(BinaryOp(FieldAccess(Id(e),x),+,IntLiteral(10)))])),FuncDecl(main,[],VoidType,Block([VarDecl(e,Id(example_t),StructLiteral(example_t,[(x,IntLiteral(10))])),FuncCall(println,[FuncCall(calc,[Id(e)])])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_31(self):
#         inp = \
#             """// Test case 31:  Boolean Expression nesting
# func main() {

# 	var x int = 10
# 	var y int = 5

# 	if (((x > 5) && (y < 10)) || (x == y)){
# 		println("True")
# 	} else {
# 		println("False")
# 	}
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,IntLiteral(10)),VarDecl(y,IntType,IntLiteral(5)),If(BinaryOp(BinaryOp(BinaryOp(Id(x),>,IntLiteral(5)),&&,BinaryOp(Id(y),<,IntLiteral(10))),||,BinaryOp(Id(x),==,Id(y))),Block([FuncCall(println,[StringLiteral("True")])]),Block([FuncCall(println,[StringLiteral("False")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_32(self):
#         inp = \
#             """// Test case 32: Missing colon in struct initialization (Error)
# type Foo struct {
#     bar int;
# }

# func main() {
#      var f Foo = Foo{bar: 5};
# }
# """
#         out = """Program([StructType(Foo,[(bar,IntType)],[]),FuncDecl(main,[],VoidType,Block([VarDecl(f,Id(Foo),StructLiteral(Foo,[(bar,IntLiteral(5))]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_33(self):
#         inp = \
#             """// Test case 34: Invalid Character in identifier (Error)
# func main() {
#     var xy int = 10;
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(xy,IntType,IntLiteral(10))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_34(self):
#         inp = \
#             """// Test case 35: Missing Return in function declared to return type
# func exampleFunc(i int ) int {
# var xy int = 10;
# }

# func main() { var xy int = 10; }
# """
#         out = """Program([FuncDecl(exampleFunc,[ParDecl(i,IntType)],IntType,Block([VarDecl(xy,IntType,IntLiteral(10))])),FuncDecl(main,[],VoidType,Block([VarDecl(xy,IntType,IntLiteral(10))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_35(self):
#         inp = \
#             """
# // Test case 35: Assigning a constant
# func main() {
#     const testConst = 12
#     testConst := 10
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([ConstDecl(testConst,IntLiteral(12)),Assign(Id(testConst),IntLiteral(10))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_36(self):
#         inp = \
#             """
# // Test case 36: More Complex struct Declaration

# type Address struct {
#   Street string
#   City string
#   Zip int
# }

# type Person struct {
#   Name string
#   Age int
#   Address Address
# }

# func main() {
#   var p Person = Person {
#     Name: "John Doe",
#     Age: 30,
#     Address: Address {
#       Street: "123 Main St",
#       City: "Anytown",
#       Zip: 12345 } }
#   println(p.Address.City)
# }
# """
#         out = """Program([StructType(Address,[(Street,StringType),(City,StringType),(Zip,IntType)],[]),StructType(Person,[(Name,StringType),(Age,IntType),(Address,Id(Address))],[]),FuncDecl(main,[],VoidType,Block([VarDecl(p,Id(Person),StructLiteral(Person,[(Name,StringLiteral("John Doe")),(Age,IntLiteral(30)),(Address,StructLiteral(Address,[(Street,StringLiteral("123 Main St")),(City,StringLiteral("Anytown")),(Zip,IntLiteral(12345))]))])),FuncCall(println,[FieldAccess(FieldAccess(Id(p),Address),City)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_37(self):
#         inp = \
#             """// Test case 37: Multiple variable declarations

# func main() {
#   if (
#     x == 10 &&
#     y == "hello" ||
#     z != 3.14
#   )
#   {println(x,y,z);}

# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([If(BinaryOp(BinaryOp(BinaryOp(Id(x),==,IntLiteral(10)),&&,BinaryOp(Id(y),==,StringLiteral("hello"))),||,BinaryOp(Id(z),!=,FloatLiteral(3.14))),Block([FuncCall(println,[Id(x),Id(y),Id(z)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_38(self):
#         inp = \
#             """// Test case 38: Global variable declaration

# var globalString string = "hello"

# func main() {
#    println(globalString)

# }
# """
#         out = """Program([VarDecl(globalString,StringType,StringLiteral("hello")),FuncDecl(main,[],VoidType,Block([FuncCall(println,[Id(globalString)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_39(self):
#         inp = \
#             """// Test case 39: For range loop
# func main() {
# 	arr := [3]int{1,2,3}
# 	for index, value := range arr {
# 		println(value)
# 	}
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([Assign(Id(arr),ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])),ForEach(Id(index),Id(value),Id(arr),Block([FuncCall(println,[Id(value)])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_40(self):
#         inp = \
#             """
# // Test case 40: Correct associativity and Precedence

# func main() {

# 	var x int = 2 * (3 + 4) / 2

# 	println(x)

# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,BinaryOp(BinaryOp(IntLiteral(2),*,BinaryOp(IntLiteral(3),+,IntLiteral(4))),/,IntLiteral(2))),FuncCall(println,[Id(x)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_41(self):
#         inp = \
#             """

# // Test case 41:  Simple Array Literal test
# func main() {
# 	var arr [3]string = [3]string{"Hello", World, {1,2,3}}

# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(arr,ArrayType(StringType,[IntLiteral(3)]),ArrayLiteral([IntLiteral(3)],StringType,[StringLiteral("Hello"),Id(World),ArrayLiteral([],VoidType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_42(self):
#         inp = \
#             """// Test case 42:  Test continue statement with label

# func main() {

# 	for i := 0; i < 10; i+= 1{
# 		if(i % 2 == 0) {
# 			continue
# 		}

# 		println(i)
# 	}

# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(i),%,IntLiteral(2)),==,IntLiteral(0)),Block([Continue()])),FuncCall(println,[Id(i)])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_43(self):
#         inp = \
#             """// Test case 43:  Nil comparison with type assertion
# func main() {
# 	var inter int = nil
# 	if (inter == nil) {
# 		println("It is nil")
# 	}
# 	}
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(inter,IntType,Nil),If(BinaryOp(Id(inter),==,Nil),Block([FuncCall(println,[StringLiteral("It is nil")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_44(self):
#         inp = \
#             """
# // Test case 44: Nested loops and branching logic

# func main() {

# 	for i := 0; i < 5; i += 1 {
# 		for j := 0; j < 5; j += 1 {
# 			if (i == j) {
# 				println("Diagonal")
# 			} else if (i > j) {
# 				println("Below Diagonal")
# 			} else {
# 				println("Above Diagonal")
# 			}
# 		}
# 	}
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(5)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([For(Assign(Id(j),IntLiteral(0)),BinaryOp(Id(j),<,IntLiteral(5)),Assign(Id(j),BinaryOp(Id(j),+,IntLiteral(1))),Block([If(BinaryOp(Id(i),==,Id(j)),Block([FuncCall(println,[StringLiteral("Diagonal")])]),If(BinaryOp(Id(i),>,Id(j)),Block([FuncCall(println,[StringLiteral("Below Diagonal")])]),Block([FuncCall(println,[StringLiteral("Above Diagonal")])])))]))]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_45(self):
#         inp = \
#             """


# // Test case 45:  Invalid type in array literal (error)
# func main() {
#    var arr [3]int = [x]int{1, "2", 3}
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(arr,ArrayType(IntType,[IntLiteral(3)]),ArrayLiteral([Id(x)],IntType,[IntLiteral(1),StringLiteral("2"),IntLiteral(3)]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_46(self):
#         inp = \
#             """// Test case 46: Variable redeclaration within inner scope (valid)
# func main() {
#     var x int = 10
#     if (true) {
#       var x string = "hello"
#       println(x)
#     }
#     println(x)
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,IntType,IntLiteral(10)),If(BooleanLiteral(true),Block([VarDecl(x,StringType,StringLiteral("hello")),FuncCall(println,[Id(x)])])),FuncCall(println,[Id(x)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_47(self):
#         inp = \
#             """// Test case 47: Missing semicolon in for loop (Error)
# func main() {
#   for i := 0 ;i < 10 ;i+=1 {
#     println(x)
#   }
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([FuncCall(println,[Id(x)])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_48(self):
#         inp = \
#             """// Test case 48: Type mismatch in assignment (Error)
# func main() {
#     var x = 0.9
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([VarDecl(x,FloatLiteral(0.9))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_49(self):
#         inp = \
#             """// Test case 49: Invalid expression in return statement (Error)
# func exampleFunc() int {
#   return "hello" + 5;
# }
# """
#         out = """Program([FuncDecl(exampleFunc,[],IntType,Block([Return(BinaryOp(StringLiteral("hello"),+,IntLiteral(5)))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_50(self):
#         inp = \
#             """ func main(){
#             for i := 0; i < 10; i += 1 {
#                 if (x % i == 0) {return false;}
#             }
#         }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(x),%,Id(i)),==,IntLiteral(0)),Block([Return(BooleanLiteral(false))]))]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_51(self):
#         inp = \
#             """func main () {return 1;}

# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([Return(IntLiteral(1))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_52(self):
#         inp = \
#             """func main(){
#             for i:=0; i <= x / 2; i += 1 {
#     if (x % i == 0) {return false
#     }
# }
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<=,BinaryOp(Id(x),/,IntLiteral(2))),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(x),%,Id(i)),==,IntLiteral(0)),Block([Return(BooleanLiteral(false))]))]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_53(self):
#         inp = \
#             """func main(x string, y float)  {
#             return 1;
# }
# """
#         out = "Program([FuncDecl(main,[ParDecl(x,StringType),ParDecl(y,FloatType)],VoidType,Block([Return(IntLiteral(1))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_54(self):
#         inp = \
#             """func foo(str string) boolean {
# writeString(str)
# var x = 7 + (t - false)
# }
# """
#         out = "Program([FuncDecl(foo,[ParDecl(str,StringType)],BoolType,Block([FuncCall(writeString,[Id(str)]),VarDecl(x,BinaryOp(IntLiteral(7),+,BinaryOp(Id(t),-,BooleanLiteral(false))))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_55(self):
#         inp = \
#             """func bar( arr int){
# x[2][8] := [3]boolean{1,2,\"3\"} + [2]string{4,\"5\",6}
# }
# """
#         out = """Program([FuncDecl(bar,[ParDecl(arr,IntType)],VoidType,Block([Assign(ArrayCell(Id(x),[IntLiteral(2),IntLiteral(8)]),BinaryOp(ArrayLiteral([IntLiteral(3)],BoolType,[IntLiteral(1),IntLiteral(2),StringLiteral("3")]),+,ArrayLiteral([IntLiteral(2)],StringType,[IntLiteral(4),StringLiteral("5"),IntLiteral(6)])))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_56(self):
#         inp = \
#             """
# func min(a int, b string){  
# if (x <= false){
#         main(a,2,\"b\")
#     }
# for var i int = 1; i <= x / 2; i += 1{ 

#     loop1(arr[a(b)][b(a)])
#     loop2(arr[a(b)],b[2])
# }

# }
# """
#         out = """Program([FuncDecl(min,[ParDecl(a,IntType),ParDecl(b,StringType)],VoidType,Block([If(BinaryOp(Id(x),<=,BooleanLiteral(false)),Block([FuncCall(main,[Id(a),IntLiteral(2),StringLiteral("b")])])),For(VarDecl(i,IntType,IntLiteral(1)),BinaryOp(Id(i),<=,BinaryOp(Id(x),/,IntLiteral(2))),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([FuncCall(loop1,[ArrayCell(Id(arr),[FuncCall(a,[Id(b)]),FuncCall(b,[Id(a)])])]),FuncCall(loop2,[ArrayCell(Id(arr),[FuncCall(a,[Id(b)])]),ArrayCell(Id(b),[IntLiteral(2)])])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_57(self):
#         inp = \
#             """func min(a int, b string){ 
# if (false) {
# doSomething(a,2,"b");}
# else if (abc > "abc") {doSomethingElif(b,true,foo(x,2))
# }
# else {doSomethingElse(doSomethingElse,foo[3.2][3]);}
# }

# """
#         out = """Program([FuncDecl(min,[ParDecl(a,IntType),ParDecl(b,StringType)],VoidType,Block([If(BooleanLiteral(false),Block([FuncCall(doSomething,[Id(a),IntLiteral(2),StringLiteral("b")])])),If(BinaryOp(Id(abc),>,StringLiteral("abc")),Block([FuncCall(doSomethingElif,[Id(b),BooleanLiteral(true),FuncCall(foo,[Id(x),IntLiteral(2)])])])),FuncCall(doSomethingElse,[Id(doSomethingElse),ArrayCell(Id(foo),[FloatLiteral(3.2),IntLiteral(3)])])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_58(self):
#         inp = \
#             """func max(a int, b number)
# {
# // Comment 1
# if (x == 6) else {doSomething();}
# // Comment 2
# }
# """
#         out = "Program([FuncDecl(max,[ParDecl(a,IntType),ParDecl(b,Id(number))],VoidType,Block([If(BinaryOp(Id(x),==,IntLiteral(6)),Block([FuncCall(doSomething,[])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_59(self):
#         inp = \
#             """func bar(arr float, b boolean) {
# x[a(b)][b(a)] := foo(1,2,\"abcd\",154/4)
# var x int= readString()
# }
# """
#         out = """Program([FuncDecl(bar,[ParDecl(arr,FloatType),ParDecl(b,BoolType)],VoidType,Block([Assign(ArrayCell(Id(x),[FuncCall(a,[Id(b)]),FuncCall(b,[Id(a)])]),FuncCall(foo,[IntLiteral(1),IntLiteral(2),StringLiteral("abcd"),BinaryOp(IntLiteral(154),/,IntLiteral(4))])),VarDecl(x,IntType,FuncCall(readString,[]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_60(self):
#         inp = \
#             """const GREETING = "Hello, World!"

# var message string

# func main() {
#     message := GREETING
#     println(message)
# }
# """
#         out = """Program([ConstDecl(GREETING,StringLiteral("Hello, World!")),VarDecl(message,StringType),FuncDecl(main,[],VoidType,Block([Assign(Id(message),Id(GREETING)),FuncCall(println,[Id(message)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_61(self):
#         inp = \
#             """var a int = 10
# var b int = 5
# var result int

# func main() {
#     result := a + b*2 - b/2
#     println(result)
# }
# """
#         out = "Program([VarDecl(a,IntType,IntLiteral(10)),VarDecl(b,IntType,IntLiteral(5)),VarDecl(result,IntType),FuncDecl(main,[],VoidType,Block([Assign(Id(result),BinaryOp(BinaryOp(Id(a),+,BinaryOp(Id(b),*,IntLiteral(2))),-,BinaryOp(Id(b),/,IntLiteral(2)))),FuncCall(println,[Id(result)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_62(self):
#         inp = \
#             """var x int = 7

# func main() {
#     if (x > 5) {
#         println("x is greater than 5")
#     } else {
#         println("x is not greater than 5")
#     }
# }
# """
#         out = """Program([VarDecl(x,IntType,IntLiteral(7)),FuncDecl(main,[],VoidType,Block([If(BinaryOp(Id(x),>,IntLiteral(5)),Block([FuncCall(println,[StringLiteral("x is greater than 5")])]),Block([FuncCall(println,[StringLiteral("x is not greater than 5")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_63(self):
#         inp = \
#             """var numbers [5]int = [5]int{1, 2, 3, 4, 5}

# func main() {
#     for arr, value := range numbers {
#         println(index, value)
#     }
# }
# """
#         out = """Program([VarDecl(numbers,ArrayType(IntType,[IntLiteral(5)]),ArrayLiteral([IntLiteral(5)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5)])),FuncDecl(main,[],VoidType,Block([ForEach(Id(arr),Id(value),Id(numbers),Block([FuncCall(println,[Id(index),Id(value)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_64(self):
#         inp = \
#             """type Point struct {
#     x int
#     y int
# }

# var p Point

# func main() {
#     p.x := 10
#     p.y := 20
#     println(p.x, p.y)
# }
# """
#         out = "Program([StructType(Point,[(x,IntType),(y,IntType)],[]),VarDecl(p,Id(Point)),FuncDecl(main,[],VoidType,Block([Assign(FieldAccess(Id(p),x),IntLiteral(10)),Assign(FieldAccess(Id(p),y),IntLiteral(20)),FuncCall(println,[FieldAccess(Id(p),x),FieldAccess(Id(p),y)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_65(self):
#         inp = \
#             """
# type Printer interface {
#     print(message string)
# }

# func main() {
#     // No implementation here to test just declaration
#     foo(5).x[2][k].y[foo(6)].abc(8.25)[false] := 10
# }

# """
#         out = "Program([InterfaceType(Printer,[Prototype(print,[StringType],VoidType)]),FuncDecl(main,[],VoidType,Block([Assign(ArrayCell(MethodCall(ArrayCell(FieldAccess(ArrayCell(FieldAccess(FuncCall(foo,[IntLiteral(5)]),x),[IntLiteral(2),Id(k)]),y),[FuncCall(foo,[IntLiteral(6)])]),abc,[FloatLiteral(8.25)]),[BooleanLiteral(false)]),IntLiteral(10))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_66(self):
#         inp = \
#             """type Rectangle struct {
#     width int
#     height int
# }

# func (r Rectangle) area() int {
#     return r.width * r.height
# }

# var rect Rectangle

# func main() {
#     rect.width := 5
#     rect.height := 10
#     println(rect.area())
# }
# """
#         out = """Program([StructType(Rectangle,[(width,IntType),(height,IntType)],[]),MethodDecl(r,Id(Rectangle),FuncDecl(area,[],IntType,Block([Return(BinaryOp(FieldAccess(Id(r),width),*,FieldAccess(Id(r),height)))]))),VarDecl(rect,Id(Rectangle)),FuncDecl(main,[],VoidType,Block([Assign(FieldAccess(Id(rect),width),IntLiteral(5)),Assign(FieldAccess(Id(rect),height),IntLiteral(10)),FuncCall(println,[MethodCall(Id(rect),area,[])])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_67(self):
#         inp = \
#             """func calculate(a int, b int) int {  // Invalid: Multiple return values
#     return a + b
# }

# func main() {
#     var sum int
#     diff := calculate(10, 5)
#     println(sum, diff)
# }
# """
#         out = "Program([FuncDecl(calculate,[ParDecl(a,IntType),ParDecl(b,IntType)],IntType,Block([Return(BinaryOp(Id(a),+,Id(b)))])),FuncDecl(main,[],VoidType,Block([VarDecl(sum,IntType),Assign(Id(diff),FuncCall(calculate,[IntLiteral(10),IntLiteral(5)])),FuncCall(println,[Id(sum),Id(diff)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_68(self):
#         inp = \
#             """var age int = 25
# var isStudent bool = false

# func main() {
#     if (age < 30) {
#         if (!isStudent) {
#             println("Young professional")
#         } else {
#             println("Young student")
#         }
#     } else {
#         println("Experienced")
#     }
# }
# """
#         out = """Program([VarDecl(age,IntType,IntLiteral(25)),VarDecl(isStudent,Id(bool),BooleanLiteral(false)),FuncDecl(main,[],VoidType,Block([If(BinaryOp(Id(age),<,IntLiteral(30)),Block([If(UnaryOp(!,Id(isStudent)),Block([FuncCall(println,[StringLiteral("Young professional")])]),Block([FuncCall(println,[StringLiteral("Young student")])]))]),Block([FuncCall(println,[StringLiteral("Experienced")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_69(self):
#         inp = \
#             """
# func main() {
#     for i := 0; i < 10; i += 1 {
#         if (i % 3 == 0) {
#             continue  // Skip multiples of 3
#         }
#         if (i > 7) {
#             break     // Exit loop if i is greater than 7
#         }
#         println(i)
#     }
#     break
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(i),%,IntLiteral(3)),==,IntLiteral(0)),Block([Continue()])),If(BinaryOp(Id(i),>,IntLiteral(7)),Block([Break()])),FuncCall(println,[Id(i)])])),Break()]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_70(self):
#         inp = \
#             """
# type Circle struct {
#     radius int
# }

# var circles [3]Circle

# func main() {
#     circles[0].radius := 5
#     circles[1].radius := 7
#     circles[2].radius := 9

#     for _, c := range circles {
#         println(c.radius)
#     }
# }
# """
#         out = "Program([StructType(Circle,[(radius,IntType)],[]),VarDecl(circles,ArrayType(Id(Circle),[IntLiteral(3)])),FuncDecl(main,[],VoidType,Block([Assign(FieldAccess(ArrayCell(Id(circles),[IntLiteral(0)]),radius),IntLiteral(5)),Assign(FieldAccess(ArrayCell(Id(circles),[IntLiteral(1)]),radius),IntLiteral(7)),Assign(FieldAccess(ArrayCell(Id(circles),[IntLiteral(2)]),radius),IntLiteral(9)),ForEach(Id(_),Id(c),Id(circles),Block([FuncCall(println,[FieldAccess(Id(c),radius)])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_71(self):
#         inp = \
#             """func main() {
#     for i < 3 {
#         for j != !1 {
#             println(i, j)
#         }
#     }
# }"""
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(BinaryOp(Id(i),<,IntLiteral(3)),Block([For(BinaryOp(Id(j),!=,UnaryOp(!,IntLiteral(1))),Block([FuncCall(println,[Id(i),Id(j)])]))]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_72(self):
#         inp = \
#             """/*
#     This is a multi-line comment.
#     It spans multiple lines.
# */

# // This is a single-line comment.

# var   x  int  =   10;  //  Declaration with extra whitespace

# func main()  {
#     //  More comments inside the function
#     println ( x  ) ;
# }
# """
#         out = "Program([VarDecl(x,IntType,IntLiteral(10)),FuncDecl(main,[],VoidType,Block([FuncCall(println,[Id(x)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_73(self):
#         inp = \
#             """var maxInt int = 2147483647  // Maximum 32-bit integer (adjust if needed)

# func main() {
#     var overflow int = maxInt + 1
#     println(overflow)  //  What happens when we overflow?
# }
# """
#         out = "Program([VarDecl(maxInt,IntType,IntLiteral(2147483647)),FuncDecl(main,[],VoidType,Block([VarDecl(overflow,IntType,BinaryOp(Id(maxInt),+,IntLiteral(1))),FuncCall(println,[Id(overflow)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_74(self):
#         inp = \
#             """ 
# var message string = "This string contains a newline and a tab\t."

# func main() {
#     println(message)
# }
# """
#         out = """Program([VarDecl(message,StringType,StringLiteral("This string contains a newline and a tab	.")),FuncDecl(main,[],VoidType,Block([FuncCall(println,[Id(message)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_75(self):
#         inp = \
#             """ 
# var x int = 5

# func main(x int, y,z float, t [2][3]int, k boolean) {
#     println(x)
# }
# """
#         out = """Program([VarDecl(x,IntType,IntLiteral(5)),FuncDecl(main,[ParDecl(x,IntType),ParDecl(y,FloatType),ParDecl(z,FloatType),ParDecl(t,ArrayType(IntType,[IntLiteral(2),IntLiteral(3)])),ParDecl(k,BoolType)],VoidType,Block([FuncCall(println,[Id(x)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_76(self):
#         inp = \
#             """var message string = "This string is not terminated"

# func main() {
#     println(message)
# }
# """
#         out = """Program([VarDecl(message,StringType,StringLiteral("This string is not terminated")),FuncDecl(main,[],VoidType,Block([FuncCall(println,[Id(message)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_77(self):
#         inp = \
#             """ 
# var x int = 5
# var y int = 10 // /* */
# func main() {
#     println(x + y)
# }
# """
#         out = "Program([VarDecl(x,IntType,IntLiteral(5)),VarDecl(y,IntType,IntLiteral(10)),FuncDecl(main,[],VoidType,Block([FuncCall(println,[BinaryOp(Id(x),+,Id(y))])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_78(self):
#         inp = \
#             """ var x int = 5

# func main() {
#     var x [1]float = Person{x: i, y: fl} // x redeclared in the same scope
#     println(x)
# }
# """
#         out = """Program([VarDecl(x,IntType,IntLiteral(5)),FuncDecl(main,[],VoidType,Block([VarDecl(x,ArrayType(FloatType,[IntLiteral(1)]),StructLiteral(Person,[(x,Id(i)),(y,Id(fl))])),FuncCall(println,[Id(x)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_79(self):
#         inp = \
#             """ var globalVar int = 20

# func myFunction() {
#     var localVar int = 10
#     println(globalVar + localVar)
# }

# func main() {
#     myFunction()
#     println([1]int{1}, [1][1]int{2}) // Access global variable from main
#     //println(localVar) // Error: localVar is not defined in main
# }
# """
#         out = """Program([VarDecl(globalVar,IntType,IntLiteral(20)),FuncDecl(myFunction,[],VoidType,Block([VarDecl(localVar,IntType,IntLiteral(10)),FuncCall(println,[BinaryOp(Id(globalVar),+,Id(localVar))])])),FuncDecl(main,[],VoidType,Block([FuncCall(myFunction,[]),FuncCall(println,[ArrayLiteral([IntLiteral(1)],IntType,[IntLiteral(1)]),ArrayLiteral([IntLiteral(1),IntLiteral(1)],IntType,[IntLiteral(2)])])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_80(self):
#         inp = \
#             """ 
# var a int = 10
# var b int = 5
# var c string = "hello"

# func main() {
#     if ((a > 5 && b < 10) || c == "world") {
#         if (a + b == 3.e+3) {
#             println("Condition met")
#         } else {
#             println("Inner condition failed")
#         }
#     } else {
#         println("Outer condition failed")
#     }
# }
# """
#         out = """Program([VarDecl(a,IntType,IntLiteral(10)),VarDecl(b,IntType,IntLiteral(5)),VarDecl(c,StringType,StringLiteral("hello")),FuncDecl(main,[],VoidType,Block([If(BinaryOp(BinaryOp(BinaryOp(Id(a),>,IntLiteral(5)),&&,BinaryOp(Id(b),<,IntLiteral(10))),||,BinaryOp(Id(c),==,StringLiteral("world"))),Block([If(BinaryOp(BinaryOp(Id(a),+,Id(b)),==,FloatLiteral(3.e+3)),Block([FuncCall(println,[StringLiteral("Condition met")])]),Block([FuncCall(println,[StringLiteral("Inner condition failed")])]))]),Block([FuncCall(println,[StringLiteral("Outer condition failed")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_81(self):
#         inp = \
#             """var x int
# var y int
# var z int

# func main() {
#     x := 1
#     y := 2 + 3
#     z := 4 * 5 - 1
#     println(x, y, z) // Illegal because it's not a function
# }"""
#         out = "Program([VarDecl(x,IntType),VarDecl(y,IntType),VarDecl(z,IntType),FuncDecl(main,[],VoidType,Block([Assign(Id(x),IntLiteral(1)),Assign(Id(y),BinaryOp(IntLiteral(2),+,IntLiteral(3))),Assign(Id(z),BinaryOp(BinaryOp(IntLiteral(4),*,IntLiteral(5)),-,IntLiteral(1))),FuncCall(println,[Id(x),Id(y),Id(z)])]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_82(self):
#         inp = \
#             """func main() {
#     for i := 0; i < 20; i+= 1 {
#         if (i % 5 == 0) {
#             continue // Skip multiples of 5
#         }
#         if (i > 3.E+5 && i < 15) {
#             break    // Exit if between 13 and 14
#         }
#         println(i)
#     }
# }
# """
#         out = """Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(20)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(BinaryOp(Id(i),%,IntLiteral(5)),==,IntLiteral(0)),Block([Continue()])),If(BinaryOp(BinaryOp(Id(i),>,FloatLiteral(3.E+5)),&&,BinaryOp(Id(i),<,IntLiteral(15))),Block([Break()])),FuncCall(println,[Id(i)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_83(self):
#         inp = \
#             """type Person struct {
#     name string
#     age int
# }

# var p Person

# func main() {
#     p.name := "Alice"
#     p.age := 0B011110 // Binary literal
#     println(p.name, p.age)
#     var message string = p.name + " is " + p.age + " years old" // Concatenation with integer will cause a type error

# }
# """
#         out = """Program([StructType(Person,[(name,StringType),(age,IntType)],[]),VarDecl(p,Id(Person)),FuncDecl(main,[],VoidType,Block([Assign(FieldAccess(Id(p),name),StringLiteral("Alice")),Assign(FieldAccess(Id(p),age),IntLiteral(0B011110)),FuncCall(println,[FieldAccess(Id(p),name),FieldAccess(Id(p),age)]),VarDecl(message,StringType,BinaryOp(BinaryOp(BinaryOp(FieldAccess(Id(p),name),+,StringLiteral(" is ")),+,FieldAccess(Id(p),age)),+,StringLiteral(" years old")))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_84(self):
#         inp = \
#             """var data = [4]int{10, 20, 30, 40}

# func main() {
#     for index, value := range data {
#         println(index * value)
#     }
#     data[index] := 
#     z; y := 10
# }
# """
#         out = "Program([VarDecl(data,ArrayLiteral([IntLiteral(4)],IntType,[IntLiteral(10),IntLiteral(20),IntLiteral(30),IntLiteral(40)])),FuncDecl(main,[],VoidType,Block([ForEach(Id(index),Id(value),Id(data),Block([FuncCall(println,[BinaryOp(Id(index),*,Id(value))])])),Assign(ArrayCell(Id(data),[Id(index)]),Id(z)),Assign(Id(y),IntLiteral(10))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_85(self):
#         inp = \
#             """
# func findValue(arr [5]int, target int) int {
#     for i := 0; i < 5; i+=1 {
#         if (arr[i] == target) {
#             return i // Return index if found
#         }
#     }
#     return -1  // Return -1 if not found
# }

# var numbers [5]int = [0O345]float{1, 2, 3, 4, 5}

# func main() {
#     var index int = findValue(numbers, 3)
#     println(index)
# }
# """
#         out = """Program([FuncDecl(findValue,[ParDecl(arr,ArrayType(IntType,[IntLiteral(5)])),ParDecl(target,IntType)],IntType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(5)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(ArrayCell(Id(arr),[Id(i)]),==,Id(target)),Block([Return(Id(i))]))])),Return(UnaryOp(-,IntLiteral(1)))])),VarDecl(numbers,ArrayType(IntType,[IntLiteral(5)]),ArrayLiteral([IntLiteral(0O345)],FloatType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5)])),FuncDecl(main,[],VoidType,Block([VarDecl(index,IntType,FuncCall(findValue,[Id(numbers),IntLiteral(3)])),FuncCall(println,[Id(index)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_86(self):
#         inp = \
#             """var x int = 10
# var y string = "hello"
# var z bool = true
# const PI = 3.14

# func main() {
#     println(x, y, z, PI)
# }
# """
#         out = """Program([VarDecl(x,IntType,IntLiteral(10)),VarDecl(y,StringType,StringLiteral("hello")),VarDecl(z,Id(bool),BooleanLiteral(true)),ConstDecl(PI,FloatLiteral(3.14)),FuncDecl(main,[],VoidType,Block([FuncCall(println,[Id(x),Id(y),Id(z),Id(PI)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_87(self):
#         inp = \
#             """type Address struct {
#     street string
#     city string
# }

# type Person struct {
#     name string
#     address Address
# }

# var p Person

# func main() {
#     p.name := "Bob"
#     p.address.street := "123 Main St"
#     p.address.city := "Anytown"
#     println(p.name, p.address.street, p.address.city)
# }
# """
#         out = """Program([StructType(Address,[(street,StringType),(city,StringType)],[]),StructType(Person,[(name,StringType),(address,Id(Address))],[]),VarDecl(p,Id(Person)),FuncDecl(main,[],VoidType,Block([Assign(FieldAccess(Id(p),name),StringLiteral("Bob")),Assign(FieldAccess(FieldAccess(Id(p),address),street),StringLiteral("123 Main St")),Assign(FieldAccess(FieldAccess(Id(p),address),city),StringLiteral("Anytown")),FuncCall(println,[FieldAccess(Id(p),name),FieldAccess(FieldAccess(Id(p),address),street),FieldAccess(FieldAccess(Id(p),address),city)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_88(self):
#         inp = \
#             """func isEven(n int) bool {
#     return n % 2 == 0
# }

# var num int = 8

# func main() {
#     if (isEven(num)) {
#         println("Even")
#     } else {
#         println("Odd")
#     }
# }
# """
#         out = """Program([FuncDecl(isEven,[ParDecl(n,IntType)],Id(bool),Block([Return(BinaryOp(BinaryOp(Id(n),%,IntLiteral(2)),==,IntLiteral(0)))])),VarDecl(num,IntType,IntLiteral(8)),FuncDecl(main,[],VoidType,Block([If(FuncCall(isEven,[Id(num)]),Block([FuncCall(println,[StringLiteral("Even")])]),Block([FuncCall(println,[StringLiteral("Odd")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_89(self):
#         inp = \
#             """var a int = 5
# var b int = 0Xab69
# var result bool

# func main() {
#     result := a + b > 12 && a * b < 60 // Will cause a type error because an int is compared to a bool
#     println(result)
# }
# """
#         out = """Program([VarDecl(a,IntType,IntLiteral(5)),VarDecl(b,IntType,IntLiteral(0Xab69)),VarDecl(result,Id(bool)),FuncDecl(main,[],VoidType,Block([Assign(Id(result),BinaryOp(BinaryOp(BinaryOp(Id(a),+,Id(b)),>,IntLiteral(12)),&&,BinaryOp(BinaryOp(Id(a),*,Id(b)),<,IntLiteral(60)))),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_90(self):
#         inp = \
#             """
# func main() {
#     for i := 0; i < 10; i/=2 { 
#         println(i) 
#     }
# }
# """
#         out = "Program([FuncDecl(main,[],VoidType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),/,IntLiteral(2))),Block([FuncCall(println,[Id(i)])]))]))])"
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_91(self):
#         inp = \
#             """
# var x int = 10

# func main() {
#     if (x > 5){
#         println("x > 5")
#     } else {
#         println("x <= 5")
#     }
# }
# """
#         out = """Program([VarDecl(x,IntType,IntLiteral(10)),FuncDecl(main,[],VoidType,Block([If(BinaryOp(Id(x),>,IntLiteral(5)),Block([FuncCall(println,[StringLiteral("x > 5")])]),Block([FuncCall(println,[StringLiteral("x <= 5")])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_92(self):
#         inp = \
#             """type MyInterface interface {
# 	doSomething()
# }
# type MyType struct{x MyInterface
# }

# func (m MyType) doSomething() {
# 	println("Hello")
# }

# func main() {
# 	var i MyInterface
# 	var m MyType
# 	i := m
#     y[6].x[0b100].doSomething()
#     Arr[i + 1] := 10

# 	//i.doSomething()// Calling method doSomething of MyInterface

# }
# """
#         out = """Program([InterfaceType(MyInterface,[Prototype(doSomething,[],VoidType)]),StructType(MyType,[(x,Id(MyInterface))],[]),MethodDecl(m,Id(MyType),FuncDecl(doSomething,[],VoidType,Block([FuncCall(println,[StringLiteral("Hello")])]))),FuncDecl(main,[],VoidType,Block([VarDecl(i,Id(MyInterface)),VarDecl(m,Id(MyType)),Assign(Id(i),Id(m)),MethodCall(ArrayCell(FieldAccess(ArrayCell(Id(y),[IntLiteral(6)]),x),[IntLiteral(0b100)]),doSomething,[]),Assign(ArrayCell(Id(Arr),[BinaryOp(Id(i),+,IntLiteral(1))]),IntLiteral(10))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_93(self):
#         inp = \
#             """
# var a bool = true
# var b bool = false
# var c bool = true

# func main() {
#     var result bool = (a && b) || (!c && a)
#     println(result)
# }
# """
#         out = """Program([VarDecl(a,Id(bool),BooleanLiteral(true)),VarDecl(b,Id(bool),BooleanLiteral(false)),VarDecl(c,Id(bool),BooleanLiteral(true)),FuncDecl(main,[],VoidType,Block([VarDecl(result,Id(bool),BinaryOp(BinaryOp(Id(a),&&,Id(b)),||,BinaryOp(UnaryOp(!,Id(c)),&&,Id(a)))),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_94(self):
#         inp = \
#             """


# var numbers [3]int = [0o27]int{1, "hello", 3} // "hello" is not an int. Error expected.

# func main() {
#     println(numbers[0], numbers[1], numbers[2])
# }
# """
#         out = """Program([VarDecl(numbers,ArrayType(IntType,[IntLiteral(3)]),ArrayLiteral([IntLiteral(0o27)],IntType,[IntLiteral(1),StringLiteral("hello"),IntLiteral(3)])),FuncDecl(main,[],VoidType,Block([FuncCall(println,[ArrayCell(Id(numbers),[IntLiteral(0)]),ArrayCell(Id(numbers),[IntLiteral(1)]),ArrayCell(Id(numbers),[IntLiteral(2)])])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_95(self):
#         inp = \
#             """var notAnArray int = 5;

# func main() {
#     for index, value := range notAnArray {
#         println(index, value);
#     }
# }
# """
#         out = """Program([VarDecl(notAnArray,IntType,IntLiteral(5)),FuncDecl(main,[],VoidType,Block([ForEach(Id(index),Id(value),Id(notAnArray),Block([FuncCall(println,[Id(index),Id(value)])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_96(self):
#         inp = \
#             """func someOtherFunction() {
#     println(x == 0x5Af)
# }
# """
#         out = """Program([FuncDecl(someOtherFunction,[],VoidType,Block([FuncCall(println,[BinaryOp(Id(x),==,IntLiteral(0x5Af))])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_97(self):
#         inp = \
#             """
#         type Circle struct {
#             radius float;
#             center Point;
#         }
#         func (c Circle) area() float {
#             return 3.14 * c.radius * c.radius;
#         }
#         func main() {
#             circles := [3]Circle{
#                 Circle{radius: 1.0, center: Point{x: 0, y: 0}},
#                 Circle{radius: 2.0, center: Point{x: 1, y: 1}},
#                 Circle{radius: 3.0, center: Point{x: 2, y: 2}} };
#         }"""
#         out = """Program([StructType(Circle,[(radius,FloatType),(center,Id(Point))],[]),MethodDecl(c,Id(Circle),FuncDecl(area,[],FloatType,Block([Return(BinaryOp(BinaryOp(FloatLiteral(3.14),*,FieldAccess(Id(c),radius)),*,FieldAccess(Id(c),radius)))]))),FuncDecl(main,[],VoidType,Block([Assign(Id(circles),ArrayLiteral([IntLiteral(3)],Id(Circle),[StructLiteral(Circle,[(radius,FloatLiteral(1.0)),(center,StructLiteral(Point,[(x,IntLiteral(0)),(y,IntLiteral(0))]))]),StructLiteral(Circle,[(radius,FloatLiteral(2.0)),(center,StructLiteral(Point,[(x,IntLiteral(1)),(y,IntLiteral(1))]))]),StructLiteral(Circle,[(radius,FloatLiteral(3.0)),(center,StructLiteral(Point,[(x,IntLiteral(2)),(y,IntLiteral(2))]))])]))]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

#     def test_ASTGen_98(self):
#         inp = \
#             """type MyType struct {
# 	Name string
# }

# func (mt MyType) someMethod() string {
# 	for i := 0; i < 10; i+=1 {
# 		if (i == 5) {
# 			return "Found 5!"
# 		}
# 	}
# 	return "Not found"
# }

# func main() {
# 	mt := MyType{Name: "Example"}
# 	result := mt[3.2e-2].f(z).someMethod()
# 	println(result)
# }
# """
#         out = """Program([StructType(MyType,[(Name,StringType)],[]),MethodDecl(mt,Id(MyType),FuncDecl(someMethod,[],StringType,Block([For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),<,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([If(BinaryOp(Id(i),==,IntLiteral(5)),Block([Return(StringLiteral("Found 5!"))]))])),Return(StringLiteral("Not found"))]))),FuncDecl(main,[],VoidType,Block([Assign(Id(mt),StructLiteral(MyType,[(Name,StringLiteral("Example"))])),Assign(Id(result),MethodCall(MethodCall(ArrayCell(Id(mt),[FloatLiteral(3.2e-2)]),f,[Id(z)]),someMethod,[])),FuncCall(println,[Id(result)])]))])"""
#         ASTGenSuite.ASTGenTest += 1
#         self.assertTrue(TestAST.checkASTGen(inp, out, ASTGenSuite.ASTGenTest))

    def test_ASTGen_99(self):
        inp = \
            """
        // const a = [2][3]int{{1, 2, 3}, {4, 5, 6}};
        var b [2][3]int;
        func main() {
            var c [2][3]int = b;
            putFloatLn(c[1][2])
        }
"""
        out = "Program([ConstDecl(a,MethodCall(Id(x),nigh,[Id(yes)]))])"
        ASTGenSuite.ASTGenTest += 1
        self.assertTrue(TestAST.checkASTGen(inp, out, 399))