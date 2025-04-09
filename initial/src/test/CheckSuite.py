import unittest
from TestUtils import TestChecker
from AST import *
import inspect

class CheckSuite(unittest.TestCase):
    def test_001(self):
        """
var Shinji = 1; 
var Shinji = 2;
        """
        input = Program([VarDecl("Shinji", None,IntLiteral(1)),VarDecl("Shinji", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: Shinji\n",401))

    def test_002(self):
        """
var Shinji = 1; 
const Shinji = 2;
        """
        input = Program([VarDecl("Shinji", None,IntLiteral(1)),ConstDecl("Shinji",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: Shinji\n",402))

    def test_003(self):
        """
const Shinji = 1; 
var Shinji = 2;
        """
        input = Program([ConstDecl("Shinji",None,IntLiteral(1)),VarDecl("Shinji", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: Shinji\n",403))

    def test_004(self):
        """
const Shinji = 1; 
func Shinji () {return;}
        """
        input = Program([ConstDecl("Shinji",None,IntLiteral(1)),FuncDecl("Shinji",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: Shinji\n",404))

    def test_005(self):
        """ 
func Shinji () {return;}
var Shinji = 1;
        """
        input = Program([FuncDecl("Shinji",[],VoidType(),Block([Return(None)])),VarDecl("Shinji", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: Shinji\n",405))

    def test_006(self):
        """ 
var getInt = 1;
        """
        input = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt\n",406))

    def test_007(self):
        """ 
type  Ikari struct {
    Ikari int;
}
type Replicant struct {
    Ikari string;
    Replicant int;
    Replicant float;
}
        """
        input = Program([StructType("Ikari",[("Ikari",IntType())],[]),StructType("Replicant",[("Ikari",StringType()),("Replicant",IntType()),("Replicant",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: Replicant\n",407))

    def test_008(self):
        """ 
func (v Replicant) putIntLn () {return;}
func (v Replicant) getInt () {return;}
func (v Replicant) getInt () {return;}
type Replicant struct {
    Ikari int;
}
        """
        input = Program([MethodDecl("v",Id("Replicant"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt\n",408))

    def test_009(self):
        """ 
type Shinji interface {
    Shinji ();
    Shinji (a int);
}
        """
        input = Program([InterfaceType("Shinji",[Prototype("Shinji",[],VoidType()),Prototype("Shinji",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: Shinji\n",409))

    def test_010(self):
        """ 
func Ikari (a, a int) {return;}
        """
        input = Program([FuncDecl("Ikari",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n",410))

    def test_011(self):
        """ 
func Ikari (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        input = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n",411))

    def test_012(self):
        """ 
func Ikari (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        input = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
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
func Ikari () int {return 1;}

func foo () {
    var b = Ikari();
    foo_Rachael();
    return;
}
        """
        input = Program([FuncDecl("Ikari",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Ikari",[])),FuncCall("foo_Rachael",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_Rachael\n",414))

    def test_015(self):
        """ 
type Replicant struct {
    Ikari int;
}

func (v Replicant) getInt () {
    const c = v.Ikari;
    var d = v.tien;
}
        """
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Ikari")),VarDecl("d", None,FieldAccess(Id("v"),"tien"))])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: tien\n",415))

    def test_016(self):
        """ 
type Replicant struct {
    Ikari int;
}

func (v Replicant) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt\n",416))

    def test_017(self):
        """ 
type Replicant struct {Ikari int;}
type Replicant struct {v int;}
        """
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),StructType("Replicant",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: Replicant\n",417))

    def test_044(self):
        """
type Replicant struct {
    Ikari int;
}
func (v Replicant) foo (v int) {return;}
func foo () {return;}"""
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("v",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "",444))

    def test_045(self):
        """
type Replicant struct {
    Ikari int;
}
func (v Replicant) foo (a, a int) {return;}
func foo () {return;}"""
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("a",IntType()), ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n",445))
    
    def test_048(self):
        input = Program([StructType("Replicant",[("Ikari",IntType())],[]),VarDecl("a", None,IntLiteral(1)),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "",448))

    def test_051(self):
        """
const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b := 2 {
        const b = 1;
    }
}"""
        input = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("b"),IntLiteral(2)),Block([ConstDecl("b",None,IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: b\n",451))


    def test_053(self):
        """
func foo () {
    const a = 1;
    for a, b := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("b", None,IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: b\n",453))

    def test_054(self):
        """
func foo () {
    const b = 1;
    for a, b := range [3]int{1, 2, 3} {
        var a = 1;
    }
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("a", None,IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: a\n",454))

    def test_055(self):
        """
func foo () {
    const b = 1;
    for a, b := range [3]int{1, 2, 3} {
        var a = 1;
    }
    var a = 1;
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("c", None,IntLiteral(1))])),VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "",455))

    def test_061(self):
        """
var a = foo();
func foo () int {
    var a =  koo();
    var c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
var d = foo();
func koo () int {
    var a =  foo ();
    return 1;
}
        """
        input = Program([VarDecl("a", None,FuncCall("foo",[])),FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,FuncCall("koo",[])),VarDecl("c", None,FuncCall("getInt",[])),FuncCall("putInt",[Id("c")]),FuncCall("putIntLn",[Id("c")]),Return(IntLiteral(1))])),VarDecl("d", None,FuncCall("foo",[])),FuncDecl("koo",[],IntType(),Block([VarDecl("a", None,FuncCall("foo",[])),Return(IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "",461))

    def test_071(self):
        """  
var v Replicant;      
type Replicant struct {
    a int;
} 
type BladeRunner interface {
    foo() int;
}

func (v Replicant) foo() int {return 1;}
func (b Replicant) koo() {b.koo();}
func foo() {
    var x BladeRunner;  
    const b = x.foo(); 
    x.koo(); 
}
        """
        input =  Program([VarDecl("v",Id("Replicant"), None),StructType("Replicant",[("a",IntType())],[]),InterfaceType("BladeRunner",[Prototype("foo",[],IntType())]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),MethodDecl("b",Id("Replicant"),FuncDecl("koo",[],VoidType(),Block([MethCall(Id("b"),"koo",[])]))),FuncDecl("foo",[],VoidType(),Block([VarDecl("x",Id("BladeRunner"), None),ConstDecl("b",None,MethCall(Id("x"),"foo",[])),MethCall(Id("x"),"koo",[])]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: koo\n",471)) 

    def test_081(self):
        """
type S1 struct {EVA_01 int;}
type S2 struct {EVA_01 int;}
type I1 interface {EVA_01(e, e int) S1;}
type I2 interface {EVA_01(a int) S1;}

func (s S1) EVA_01(a, b int) S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        """
        input = Program([StructType("S1",[("EVA_01",IntType())],[]),StructType("S2",[("EVA_01",IntType())],[]),InterfaceType("I1",[Prototype("EVA_01",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("EVA_01",[IntType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("EVA_01",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: EVA_01\n",481))

    def test_086(self):
        """
func foo(){
    if (true) {
         var a float = 1.02;
    } else {
        var a int = 1.02;
    }
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([If(BooleanLiteral("true"), Block([VarDecl("a",FloatType(),FloatLiteral(1.02))]), Block([VarDecl("a",IntType(),FloatLiteral(1.02))]))]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.02))\n",486))

    def test_092(self):
        """
func foo(){
    return
}
func foo1() int{
    return 1
}
func foo2() float{
    return 2
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([Return(None)])),FuncDecl("foo1",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo2",[],FloatType(),Block([Return(IntLiteral(2))]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: Return(IntLiteral(2))\n""",492))

    def test_093(self):
        """
var a = [2] int {1, 2}
var c [2] float = a
        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(2)],FloatType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, "",493))

    def test_107(self):
        input = """
type S1 struct {EVA_01 int;}
type I1 interface {EVA_01();}
var a I1;
var c I1;
var d S1;
func foo(){
    c := a;
    d := S1{EVA_01:8};
}

var e int = 6.0;
        """
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(e,IntType,FloatLiteral(6.0))\n""",507))

    def test_116(self):
        """
var a boolean = true && false || true;
var b boolean = true && 1;
        """
        input = Program([VarDecl("a",BoolType(),BinaryOp("||", BinaryOp("&&", BooleanLiteral("True"), BooleanLiteral("False")), BooleanLiteral("True"))),VarDecl("b",BoolType(),BinaryOp("&&", BooleanLiteral("True"), IntLiteral(1)))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp(BooleanLiteral(true),&&,IntLiteral(1))\n""",516))

    def test_117(self):
        """
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
        """
        input = Program([VarDecl("a",BoolType(),BinaryOp(">", IntLiteral(1), IntLiteral(2))),VarDecl("b",BoolType(),BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),VarDecl("c",BoolType(),BinaryOp("==", StringLiteral("""1"""), StringLiteral("""2"""))),VarDecl("d",BoolType(),BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp(IntLiteral(1),>,FloatLiteral(2.0))\n""",517))

    def test_143(self):
        """
var a Replicant;
func foo() Replicant {
    return a;
    return Replicant;
}

type Replicant struct {tien int;}
        """
        input =  Program([VarDecl("a",Id("Replicant"), None),FuncDecl("foo",[],Id("Replicant"),Block([Return(Id("a")),Return(Id("Replicant"))])),StructType("Replicant",[("tien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: Replicant\n""",543)) 

    def test_151(self):
        """
type putLn struct {a int;};
        """
        input = Program([StructType("putLn",[("a",IntType())],[])])
        self.assertTrue(TestChecker.test(input, """Redeclared Type: putLn\n""",551))

    def test_152(self):
        """
type putLn interface {foo();};
        """
        input = Program([InterfaceType("putLn",[Prototype("foo",[],VoidType())])])
        self.assertTrue(TestChecker.test(input, """Redeclared Type: putLn\n""",552))

    def test_153(self):
        """
var a int = getBool();
        """
        input = Program([VarDecl("a",IntType(),FuncCall("getBool",[]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(a,IntType,FuncCall(getBool,[]))\n""",553))

    def test_154(self):
        """
func foo() {
    putFloat(getInt());
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([FuncCall("putFloat",[FuncCall("getInt",[])])]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall(putFloat,[FuncCall(getInt,[])])\n""",554))

    def test_167(self):
        """
func foo() int {
    var a = 1;
    if (a < 3) {
        var a = 1;
    } else if(a > 2) {
        var a = 2;
    }
    return a;
}
        """
        input = Program([FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,IntLiteral(1)),If(BinaryOp("<", Id("a"), IntLiteral(3)), Block([VarDecl("a", None,IntLiteral(1))]), If(BinaryOp(">", Id("a"), IntLiteral(2)), Block([VarDecl("a", None,IntLiteral(2))]), None)),Return(Id("a"))]))])
        self.assertTrue(TestChecker.test(input, "",567))

    def test_174(self):
        """
var A = 1;
type A struct {a int;}
        """
        input =  Program([VarDecl("A", None,IntLiteral(1)),StructType("A",[("a",IntType())],[])])
        self.assertTrue(TestChecker.test(input, """Redeclared Type: A\n""",574)) 

    def test_182(self):
        """
type S1 struct {EVA_01 int;}
type I1 interface {EVA_01();}

func (s S1) EVA_01() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        input = Program([StructType("S1",[("EVA_01",IntType())],[]),InterfaceType("I1",[Prototype("EVA_01",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("EVA_01",[],VoidType(),Block([Return(None)]))),VarDecl("b",ArrayType([IntLiteral(2)],Id("S1")), None),VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: EVA_01\n""",582)) 

    def test_184(self):
        """
var a [10] int;
var b [10] int = a;
        """
        input =  Program([VarDecl("a",ArrayType([IntLiteral(10)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, """""",584)) 

    def test_185(self):
        """
var a [10] int;
var b [10] int = a;
        """
        input =  Program([VarDecl("a",ArrayType([IntLiteral(10)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, """""",585)) 

    def test_186(self):
        """
var a [2] int;
var b [5] int = a;
        """
        input =  Program([VarDecl("a",ArrayType([IntLiteral(2)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(5)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(b,ArrayType(IntType,[IntLiteral(5)]),Id(a))\n""",586)) 

    def test_187(self):
        """
var a [d] int;
var b [1] int = a;
        """
        input =  Program([VarDecl("a",ArrayType([Id("d")],IntType()), None),VarDecl("b",ArrayType([IntLiteral(1)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: d\n""",587)) 

    def test_189(self):
        """
const a = 2 + 3;
var b [a * 2 + a] int;
var c [16] int = b;
        """
        input =  Program([ConstDecl("a",None,BinaryOp("+", IntLiteral(2), IntLiteral(3))),VarDecl("b",ArrayType([BinaryOp("+", BinaryOp("*", Id("a"), IntLiteral(2)), Id("a"))],IntType()), None),VarDecl("c",ArrayType([IntLiteral(15)],IntType()),Id("b"))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(c,ArrayType(IntType,[IntLiteral(16)]),Id(b))\n""",589)) 

    def test_192(self):
        input = """
const v = 3;
const k = v + 1;
func foo(a [3] int) {
    foo([k] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall(foo,[ArrayLiteral([Id(k)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])""",592))

    def test_194(self):
        input = """
type K struct {a int;}
func (k K) koo(a [3] int) {return;}
type H interface {koo(a [3] int);}

const c = 3;
func foo() {
    var k H;
    k.koo([c] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(input, """""",594)) 

    def test_196(self):
        """
const a = "2" + "#";
const b = a * 5;
        """
        input =  Program([ConstDecl("a",None,BinaryOp("+", StringLiteral("""2"""), StringLiteral("""#"""))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5)))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp(Id(a),*,IntLiteral(5))\n""",596)) 

    def test_197(self):
        """
var v = 2 * 3;
const a = v + 1;
const b = a * 5;
const c = ! (b > 3);
        """
        input =  Program([VarDecl("v", None,BinaryOp("*", IntLiteral(2), IntLiteral(3))),ConstDecl("a",None,BinaryOp("+", Id("v"), IntLiteral(1))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5))),ConstDecl("c",None,UnaryOp("!",BinaryOp(">", Id("b"), IntLiteral(3))))])
        self.assertTrue(TestChecker.test(input, "",597)) 

    def test_199(self):
        """
const a = 3;
const b = -a;
const c = -b;
var d [c] int = [3] int {1,2,3}
        """
        input =  Program([ConstDecl("a",None,IntLiteral(3)),ConstDecl("b",None,UnaryOp("-",Id("a"))),ConstDecl("c",None,UnaryOp("-",Id("b"))),VarDecl("d",ArrayType([Id("c")],IntType()),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        self.assertTrue(TestChecker.test(input, """""",599))

    def test_202(self):
        """
func foo() {
    a := 1;
    var a = 1;
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),IntLiteral(1)),VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, """Redeclared Variable: a\n""",602)) 
    
    def test_204(self):
        """
const a = 1;
func foo() {
    a := 1.;
}
        """
        input = Program([ConstDecl("a",None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),FloatLiteral(1.0))]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: Assign(Id(a),FloatLiteral(1.0))\n""",604)) 

    def test_208(self):
        """
func Ikari (b int) {
    for var a = 1; c < 1; a += c {
        const c = 2;
    }
}
        """
        input = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("c"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), Id("c"))),Block([ConstDecl("c",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c\n""",608)) 

    def test_210(self):
        """
var v Replicant;
func (v Replicant) foo (v int) int {
    return v;
}

type Replicant struct {
    Ikari int;
}
        """
        input = Program([VarDecl("v",Id("Replicant"), None),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("v",IntType())],IntType(),Block([Return(Id("v"))]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "",610))

    def test_212(self):
        """
func (v Replicant) Ikari () {return ;}
type Replicant struct {
    Ikari int;
}
        """
        input = Program([MethodDecl("v",Id("Replicant"),FuncDecl("Ikari",[],VoidType(),Block([Return(None)]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: Ikari\n",612))

    def test_225(self):
        """
func foo() {
    foo := 1;
    foo()
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("foo"),IntLiteral(1)),FuncCall("foo",[])]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Assign(Id(foo),IntLiteral(1))\n",625))