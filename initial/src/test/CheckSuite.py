import unittest
from TestUtils import TestChecker
from AST import *
import inspect

class CheckSuite(unittest.TestCase):
    def test_001(self):
        """
var VoTien = 1; 
var VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n",401))

    def test_002(self):
        """
var VoTien = 1; 
const VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),ConstDecl("VoTien",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: VoTien\n",402))

    def test_003(self):
        """
const VoTien = 1; 
var VoTien = 2;
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n",403))

    def test_004(self):
        """
const VoTien = 1; 
func VoTien () {return;}
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),FuncDecl("VoTien",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: VoTien\n",404))

    def test_005(self):
        """ 
func VoTien () {return;}
var VoTien = 1;
        """
        input = Program([FuncDecl("VoTien",[],VoidType(),Block([Return(None)])),VarDecl("VoTien", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n",405))

    def test_006(self):
        """ 
var getInt = 1;
        """
        input = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt\n",406))

    def test_007(self):
        """ 
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
        """
        input = Program([StructType("Votien",[("Votien",IntType())],[]),StructType("TIEN",[("Votien",StringType()),("TIEN",IntType()),("TIEN",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: TIEN\n",407))

    def test_008(self):
        """ 
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt\n",408))

    def test_009(self):
        """ 
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
        """
        input = Program([InterfaceType("VoTien",[Prototype("VoTien",[],VoidType()),Prototype("VoTien",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: VoTien\n",409))

    def test_010(self):
        """ 
func Votien (a, a int) {return;}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n",410))

    def test_011(self):
        """ 
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n",411))

    def test_012(self):
        """ 
func Votien (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n",412))

    def test_013(self):
        """ 
var a = 1;
var b = a;
var c = d;
        """
        input = Program([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,Id("a")),VarDecl("c", None,Id("d"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: d\n",413))

    def test_014(self):
        """ 
func Votien () int {return 1;}

func foo () {
    var b = Votien();
    foo_votine();
    return;
}
        """
        input = Program([FuncDecl("Votien",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Votien",[])),FuncCall("foo_votine",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_votine\n",414))

    def test_015(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Votien")),VarDecl("d", None,FieldAccess(Id("v"),"tien"))])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: tien\n",415))

    def test_016(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt\n",416))

    def test_017(self):
        """ 
type TIEN struct {Votien int;}
type TIEN struct {v int;}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),StructType("TIEN",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN\n",417))

#     def test_044(self):
#         """
# type TIEN struct {
#     Votien int;
# }
# func (v TIEN) foo (v int) {return;}
# func foo () {return;}"""
#         input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("v",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
#         self.assertTrue(TestChecker.test(input, "VOTIEN\n",40))

#     def test_045(self):
#         """
# type TIEN struct {
#     Votien int;
# }
# func (v TIEN) foo (a, a int) {return;}
# func foo () {return;}"""
#         input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("a",IntType()), ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
#         self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n",40))
    
#     def test_048(self):
#         input = Program([StructType("TIEN",[("Votien",IntType())],[]),VarDecl("a", None,IntLiteral(1)),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))])
#         self.assertTrue(TestChecker.test(input, "VOTIEN\n",40))

#     def test_051(self):
#         """
# const a = 2;
# func foo () {
#     const a = 1;
#     for var a = 1; a < 1; b := 2 {
#         const b = 1;
#     }
# }"""
#         input = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("b"),IntLiteral(2)),Block([ConstDecl("b",None,IntLiteral(1))]))]))])
#         self.assertTrue(TestChecker.test(input, "Redeclared Constant: b\n",40))


#     def test_053(self):
#         """
# func foo () {
#     const a = 1;
#     for a, b := range [3]int {1, 2, 3} {
#         var b = 1;
#     }
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("b", None,IntLiteral(1))]))]))])
#         self.assertTrue(TestChecker.test(input, "Redeclared Variable: b\n",40))

#     def test_054(self):
#         """
# func foo () {
#     const b = 1;
#     for a, b := range [3]int{1, 2, 3} {
#         var a = 1;
#     }
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("a", None,IntLiteral(1))]))]))])
#         self.assertTrue(TestChecker.test(input, "Redeclared Variable: a\n",40))

#     def test_055(self):
#         """
# func foo () {
#     const b = 1;
#     for a, b := range [3]int{1, 2, 3} {
#         var a = 1;
#     }
#     var a = 1;
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("c", None,IntLiteral(1))])),VarDecl("a", None,IntLiteral(1))]))])
#         self.assertTrue(TestChecker.test(input, "VOTIEN\n",40))

#     def test_061(self):
#         """
# var a = foo();
# func foo () int {
#     var a =  koo();
#     var c = getInt();
#     putInt(c);
#     putIntLn(c);
#     return 1;
# }
# var d = foo();
# func koo () int {
#     var a =  foo ();
#     return 1;
# }
#         """
#         input = Program([VarDecl("a", None,FuncCall("foo",[])),FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,FuncCall("koo",[])),VarDecl("c", None,FuncCall("getInt",[])),FuncCall("putInt",[Id("c")]),FuncCall("putIntLn",[Id("c")]),Return(IntLiteral(1))])),VarDecl("d", None,FuncCall("foo",[])),FuncDecl("koo",[],IntType(),Block([VarDecl("a", None,FuncCall("foo",[])),Return(IntLiteral(1))]))])
#         self.assertTrue(TestChecker.test(input, "VOTIEN\n",40))

#     def test_071(self):
#         """  
# var v TIEN;      
# type TIEN struct {
#     a int;
# } 
# type VO interface {
#     foo() int;
# }

# func (v TIEN) foo() int {return 1;}
# func (b TIEN) koo() {b.koo();}
# func foo() {
#     var x VO;  
#     const b = x.foo(); 
#     x.koo(); 
# }
#         """
#         input =  Program([VarDecl("v",Id("TIEN"), None),StructType("TIEN",[("a",IntType())],[]),InterfaceType("VO",[Prototype("foo",[],IntType())]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),MethodDecl("b",Id("TIEN"),FuncDecl("koo",[],VoidType(),Block([MethCall(Id("b"),"koo",[])]))),FuncDecl("foo",[],VoidType(),Block([VarDecl("x",Id("VO"), None),ConstDecl("b",None,MethCall(Id("x"),"foo",[])),MethCall(Id("x"),"koo",[])]))])
#         self.assertTrue(TestChecker.test(input, "Undeclared Method: koo\n",40)) 

#     def test_054(self):
#         """
# func foo () {
#     const b = 1;
#     for a, b := range [3]int{1, 2, 3} {
#         var a = 1;
#     }
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("a", None,IntLiteral(1))]))]))])
#         self.assertTrue(TestChecker.test(input, "Redeclared Variable: a\n",40))

#     def test_081(self):
#         """
# type S1 struct {votien int;}
# type S2 struct {votien int;}
# type I1 interface {votien(e, e int) S1;}
# type I2 interface {votien(a int) S1;}

# func (s S1) votien(a, b int) S1 {return s;}

# var a S1;
# var c I1 = a;
# var d I2 = a;
#         """
#         input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("votien",[IntType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("votien",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("d",Id("I2"),Id("a"))""\n",40))

#     def test_086(self):
#         """
# func foo(){
#     if (true) {
#          var a float = 1.02;
#     } else {
#         var a int = 1.02;
#     }
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([If(BooleanLiteral("true"), Block([VarDecl("a",FloatType(),FloatLiteral(1.02))]), Block([VarDecl("a",IntType(),FloatLiteral(1.02))]))]))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("a",IntType(),FloatLiteral(1.02))""\n",40))

#     def test_092(self):
#         """
# func foo(){
#     return
# }
# func foo1() int{
#     return 1
# }
# func foo2() float{
#     return 2
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([Return(None)])),FuncDecl("foo1",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo2",[],FloatType(),Block([Return(IntLiteral(2))]))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: Return(IntLiteral(2))""\n",40))

#     def test_093(self):
#         """
# var a = [2] int {1, 2}
# var c [2] float = a
#         """
#         input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(2)],FloatType()),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40))

#     def test_107(self):
#         """
# type S1 struct {votien int;}
# type I1 interface {votien();}
# var a I1;
# var c I1 = nil;
# var d S1 = nil;
# func foo(){
#     c := a;
#     a := nil;
# }

# var e int = nil;
#         """
#         input = Program([StructType("S1",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),VarDecl("a",Id("I1"), None),VarDecl("c",Id("I1"),NilLiteral()),VarDecl("d",Id("S1"),NilLiteral()),FuncDecl("foo",[],VoidType(),Block([Assign(Id("c"),Id("a")),Assign(Id("a"),NilLiteral())])),VarDecl("e",IntType(),NilLiteral())])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",IntType(),NilLiteral())""\n",40))

#     def test_116(self):
#         """
# var a boolean = true && false || true;
# var b boolean = true && 1;
#         """
#         input = Program([VarDecl("a",BoolType(),BinaryOp("||", BinaryOp("&&", BooleanLiteral("True"), BooleanLiteral("False")), BooleanLiteral("True"))),VarDecl("b",BoolType(),BinaryOp("&&", BooleanLiteral("True"), IntLiteral(1)))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp("&&", BooleanLiteral(true), IntLiteral(1))""\n",40))

#     def test_117(self):
#         """
# var a boolean = 1 > 2;
# var b boolean = 1.0 < 2.0;
# var c boolean = "1" == "2";
# var d boolean = 1 > 2.0;
#         """
#         input = Program([VarDecl("a",BoolType(),BinaryOp(">", IntLiteral(1), IntLiteral(2))),VarDecl("b",BoolType(),BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),VarDecl("c",BoolType(),BinaryOp("==", StringLiteral("""1"""), StringLiteral("""2"""))),VarDecl("d",BoolType(),BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp(">", IntLiteral(1), FloatLiteral(2.0))""\n",40))

#     def test_143(self):
#         """
# var a TIEN;
# func foo() TIEN {
#     return a;
#     return TIEN;
# }

# type TIEN struct {tien int;}
#         """
#         input =  Program([VarDecl("a",Id("TIEN"), None),FuncDecl("foo",[],Id("TIEN"),Block([Return(Id("a")),Return(Id("TIEN"))])),StructType("TIEN",[("tien",IntType())],[])])
#         self.assertTrue(TestChecker.test(input, """Undeclared Identifier: TIEN""\n",40)) 

#     def test_151(self):
#         """
# type putLn struct {a int;};
#         """
#         input = Program([StructType("putLn",[("a",IntType())],[])])
#         self.assertTrue(TestChecker.test(input, """Redeclared Type: putLn""\n",40))

#     def test_152(self):
#         """
# type putLn interface {foo();};
#         """
#         input = Program([InterfaceType("putLn",[Prototype("foo",[],VoidType())])])
#         self.assertTrue(TestChecker.test(input, """Redeclared Type: putLn""\n",40))

#     def test_153(self):
#         """
# var a int = getBool();
#         """
#         input = Program([VarDecl("a",IntType(),FuncCall("getBool",[]))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("a",IntType(),FuncCall("getBool",[]))""\n",40))

#     def test_154(self):
#         """
# func foo() {
#     putFloat(getInt());
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([FuncCall("putFloat",[FuncCall("getInt",[])])]))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall("putFloat",[FuncCall("getInt",[])])""\n",40))

#     def test_167(self):
#         """
# func foo() int {
#     var a = 1;
#     if (a < 3) {
#         var a = 1;
#     } else if(a > 2) {
#         var a = 2;
#     }
#     return a;
# }
#         """
#         input = Program([FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,IntLiteral(1)),If(BinaryOp("<", Id("a"), IntLiteral(3)), Block([VarDecl("a", None,IntLiteral(1))]), If(BinaryOp(">", Id("a"), IntLiteral(2)), Block([VarDecl("a", None,IntLiteral(2))]), None)),Return(Id("a"))]))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40))

#     def test_174(self):
#         """
# var A = 1;
# type A struct {a int;}
#         """
#         input =  Program([VarDecl("A", None,IntLiteral(1)),StructType("A",[("a",IntType())],[])])
#         self.assertTrue(TestChecker.test(input, """Redeclared Type: A""\n",40)) 

#     def test_182(self):
#         """
# type S1 struct {votien int;}
# type I1 interface {votien();}

# func (s S1) votien() {return;}

# var b [2] S1;
# var a [2] I1 = b;
#         """
#         input = Program([StructType("S1",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("b",ArrayType([IntLiteral(2)],Id("S1")), None),VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))""\n",40)) 

#     def test_184(self):
#         """
# var a [1 + 9] int;
# var b [10] int = a;
#         """
#         input =  Program([VarDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_185(self):
#         """
# var a [2 * 5] int;
# var b [10] int = a;
#         """
#         input =  Program([VarDecl("a",ArrayType([BinaryOp("*", IntLiteral(2), IntLiteral(5))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_186(self):
#         """
# var a [5 / 2] int;
# var b [5] int = a;
#         """
#         input =  Program([VarDecl("a",ArrayType([BinaryOp("/", IntLiteral(5), IntLiteral(2))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(2)],IntType()),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_187(self):
#         """
# var a [5 % 2] int;
# var b [1] int = a;
#         """
#         input =  Program([VarDecl("a",ArrayType([BinaryOp("%", IntLiteral(5), IntLiteral(2))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(1)],IntType()),Id("a"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_189(self):
#         """
# const a = 2 + 3;
# var b [a * 2 + a] int;
# var c [15] int = b;
#         """
#         input =  Program([ConstDecl("a",None,BinaryOp("+", IntLiteral(2), IntLiteral(3))),VarDecl("b",ArrayType([BinaryOp("+", BinaryOp("*", Id("a"), IntLiteral(2)), Id("a"))],IntType()), None),VarDecl("c",ArrayType([IntLiteral(15)],IntType()),Id("b"))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_192(self):
#         """
# const v = 3;
# const k = v + 1;
# func foo(a [1 + 2] int) {
#     foo([k - 1] int {1,2,3})
# } 
#         """
#         input =  Program([ConstDecl("v",None,IntLiteral(3)),ConstDecl("k",None,BinaryOp("+", Id("v"), IntLiteral(1))),FuncDecl("foo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([FuncCall("foo",[ArrayLiteral([BinaryOp("-", Id("k"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40))

#     def test_194(self):
#         """
# type K struct {a int;}
# func (k K) koo(a [1 + 2] int) {return;}
# type H interface {koo(a [1 + 2] int);}

# const c = 4;
# func foo() {
#     var k H;
#     k.koo([c - 1] int {1,2,3})
# } 
#         """
#         input =  Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([Return(None)]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],VoidType())]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],VoidType(),Block([VarDecl("k",Id("H"), None),MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_196(self):
#         """
# const a = "2" + "#";
# const b = a * 5;
#         """
#         input =  Program([ConstDecl("a",None,BinaryOp("+", StringLiteral("""2"""), StringLiteral("""#"""))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5)))])
#         self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp("*", Id("a"), IntLiteral(5))""\n",40)) 

#     def test_197(self):
#         """
# var v = 2 * 3;
# const a = v + 1;
# const b = a * 5;
# const c = ! (b > 3);
#         """
#         input =  Program([VarDecl("v", None,BinaryOp("*", IntLiteral(2), IntLiteral(3))),ConstDecl("a",None,BinaryOp("+", Id("v"), IntLiteral(1))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5))),ConstDecl("c",None,UnaryOp("!",BinaryOp(">", Id("b"), IntLiteral(3))))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40)) 

#     def test_199(self):
#         """
# const a = 3;
# const b = -a;
# const c = -b;
# var d [c] int = [3] int {1,2,3}
#         """
#         input =  Program([ConstDecl("a",None,IntLiteral(3)),ConstDecl("b",None,UnaryOp("-",Id("a"))),ConstDecl("c",None,UnaryOp("-",Id("b"))),VarDecl("d",ArrayType([Id("c")],IntType()),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
#         self.assertTrue(TestChecker.test(input, """VOTIEN""\n",40))

#     def test_202(self):
#         """
# func foo() {
#     a := 1;
#     var a = 1;
# }
#         """
#         input = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),IntLiteral(1)),VarDecl("a", None,IntLiteral(1))]))])
#         print('TEST 202 NHA')
#         self.assertTrue(TestChecker.test(input, """Redeclared Variable: a""\n",40)) 

#     def test_208(self):
#         """
# func Votien (b int) {
#     for var a = 1; c < 1; a += c {
#         const c = 2;
#     }
# }
#         """
#         input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("c"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), Id("c"))),Block([ConstDecl("c",None,IntLiteral(2))]))]))])
#         self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c""\n",40)) 

#     def test_210(self):
#         """
# var v TIEN;
# func (v TIEN) foo (v int) int {
#     return v;
# }

# type TIEN struct {
#     Votien int;
# }
#         """
#         input = Program([VarDecl("v",Id("TIEN"), None),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("v",IntType())],IntType(),Block([Return(Id("v"))]))),StructType("TIEN",[("Votien",IntType())],[])])
#         self.assertTrue(TestChecker.test(input, "VOTIEN\n",40))