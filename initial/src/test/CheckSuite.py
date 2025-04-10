import unittest
from TestUtils import TestChecker
from AST import *
import inspect

class CheckSuite(unittest.TestCase):
        
    def testChecker_00(self):
        inp = \
            """func max(a int, b string) int
{
var x = 5
// Comment 1
if (x == 6) else {max(a, b);}
// Comment 2
}
"""
        out = "Type Mismatch: FuncCall(max,[Id(a),Id(b)])\n"
        self.assertTrue(TestChecker.test(inp, out, 400))

    def testChecker_01(self):
        """
var Shinji = 1; 
var Shinji = 2;
        """
        inp = Program([VarDecl("Shinji", None,IntLiteral(1)),VarDecl("Shinji", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Variable: Shinji\n",401))

    def testChecker_02(self):
        """
var Shinji = 1; 
const Shinji = 2;
        """
        inp = Program([VarDecl("Shinji", None,IntLiteral(1)),ConstDecl("Shinji",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Constant: Shinji\n",402))

    def testChecker_03(self):
        """
const Shinji = 1; 
var Shinji = 2;
        """
        inp = Program([ConstDecl("Shinji",None,IntLiteral(1)),VarDecl("Shinji", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Variable: Shinji\n",403))

    def testChecker_04(self):
        """
const Shinji = 1; 
func Shinji () {return;}
        """
        inp = Program([ConstDecl("Shinji",None,IntLiteral(1)),FuncDecl("Shinji",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Function: Shinji\n",404))

    def testChecker_05(self):
        """ 
func Shinji () {return;}
var Shinji = 1;
        """
        inp = Program([FuncDecl("Shinji",[],VoidType(),Block([Return(None)])),VarDecl("Shinji", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Variable: Shinji\n",405))

    def testChecker_06(self):
        """ 
var getInt = 1;
        """
        inp = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Variable: getInt\n",406))

    def testChecker_07(self):
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
        inp = Program([StructType("Ikari",[("Ikari",IntType())],[]),StructType("Replicant",[("Ikari",StringType()),("Replicant",IntType()),("Replicant",FloatType())],[])])
        self.assertTrue(TestChecker.test(inp, "Redeclared Field: Replicant\n",407))

    def testChecker_08(self):
        """ 
func (v Replicant) putIntLn () {return;}
func (v Replicant) getInt () {return;}
func (v Replicant) getInt () {return;}
type Replicant struct {
    Ikari int;
}
        """
        inp = Program([MethodDecl("v",Id("Replicant"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, "Redeclared Method: getInt\n",408))

    def testChecker_09(self):
        """ 
type Shinji interface {
    Shinji ();
    Shinji (a int);
}
        """
        inp = Program([InterfaceType("Shinji",[Prototype("Shinji",[],VoidType()),Prototype("Shinji",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(inp, "Redeclared Prototype: Shinji\n",409))

    def testChecker_10(self):
        """ 
func Ikari (a, a int) {return;}
        """
        inp = Program([FuncDecl("Ikari",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Parameter: a\n",410))

    def testChecker_11(self):
        """ 
func Ikari (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        inp = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Constant: a\n",411))

    def testChecker_12(self):
        """ 
func Ikari (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        inp = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Constant: a\n",412))

    def testChecker_13(self):
        """ 
var a = 1;
var b = a;
var c = d;
        """
        inp = Program([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,Id("a")),VarDecl("c", None,Id("d"))])
        self.assertTrue(TestChecker.test(inp, "Undeclared Identifier: d\n",413))

    def testChecker_14(self):
        """ 
func Ikari () int {return 1;}

func foo () {
    var b = Ikari();
    foo_Rachael();
    return;
}
        """
        inp = Program([FuncDecl("Ikari",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Ikari",[])),FuncCall("foo_Rachael",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(inp, "Undeclared Function: foo_Rachael\n",414))

    def testChecker_15(self):
        """ 
type Replicant struct {
    Ikari int;
}

func (v Replicant) getInt () {
    const c = v.Ikari;
    var d = v.Nosferatu;
}
        """
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Ikari")),VarDecl("d", None,FieldAccess(Id("v"),"Nosferatu"))])))])
        self.assertTrue(TestChecker.test(inp, "Undeclared Field: Nosferatu\n",415))

    def testChecker_16(self):
        """ 
type Replicant struct {
    Ikari int;
}

func (v Replicant) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(inp, "Undeclared Method: putInt\n",416))

    def testChecker_17(self):
        """ 
type Replicant struct {Ikari int;}
type Replicant struct {v int;}
        """
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),StructType("Replicant",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, "Redeclared Type: Replicant\n",417))

    def testChecker_18(self):
        inp = \
            """// Test case 1: String manipulation and conditional output
func main() {
    var name string = "MiniGo";
    var greeting string = "Hello, " + name + "!";
    if (len(greeting) > 10) {
        putString(greeting)
    }
}
"""
        out = """Undeclared Function: len\n"""
        self.assertTrue(TestChecker.test(inp, out, 418))

    def testChecker_19(self):
        """
type Replicant struct {
    Ikari int;
}
func (v Replicant) foo (v int) {return;}
func foo () {return;}"""
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("v",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(inp, "",419))

    def testChecker_20(self):
        """
type Replicant struct {
    Ikari int;
}
func (v Replicant) foo (a, a int) {return;}
func foo () {return;}"""
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("a",IntType()), ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Parameter: a\n",420))
    
    def testChecker_21(self):
        inp = Program([StructType("Replicant",[("Ikari",IntType())],[]),VarDecl("a", None,IntLiteral(1)),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))),FuncDecl("foo",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],VoidType(),Block([VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(inp, "",421))

    def testChecker_22(self):
        """
const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b := 2 {
        const b = 1;
    }
}"""
        inp = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("b"),IntLiteral(2)),Block([ConstDecl("b",None,IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Constant: b\n",422))


    def testChecker_23(self):
        inp = """
func foo () {
    const a = 1;
    for _, a := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(inp, "",423))

    def testChecker_24(self):
        inp = """
func foo () {
    const b = 1.0;
    var a int;
    for a, b := range [3]int{1, 2, 3} {
        var a = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(inp, "Type Mismatch: ForEach(Id(a),Id(b),ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl(a,IntLiteral(1))]))\n",424))

    def testChecker_25(self):
        inp = """
func foo () {
    const b = 1;
    for a, b := range [3]int{1, 2, 3} {
        var a = 1;
    }
    var a = 1;
}
        """
        self.assertTrue(TestChecker.test(inp, "Undeclared Identifier: a\n",425))

    def testChecker_26(self):
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
        inp = Program([VarDecl("a", None,FuncCall("foo",[])),FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,FuncCall("koo",[])),VarDecl("c", None,FuncCall("getInt",[])),FuncCall("putInt",[Id("c")]),FuncCall("putIntLn",[Id("c")]),Return(IntLiteral(1))])),VarDecl("d", None,FuncCall("foo",[])),FuncDecl("koo",[],IntType(),Block([VarDecl("a", None,FuncCall("foo",[])),Return(IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(inp, "",426))

    def testChecker_27(self):
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
        inp =  Program([VarDecl("v",Id("Replicant"), None),StructType("Replicant",[("a",IntType())],[]),InterfaceType("BladeRunner",[Prototype("foo",[],IntType())]),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),MethodDecl("b",Id("Replicant"),FuncDecl("koo",[],VoidType(),Block([MethCall(Id("b"),"koo",[])]))),FuncDecl("foo",[],VoidType(),Block([VarDecl("x",Id("BladeRunner"), None),ConstDecl("b",None,MethCall(Id("x"),"foo",[])),MethCall(Id("x"),"koo",[])]))])
        self.assertTrue(TestChecker.test(inp, "Undeclared Method: koo\n",427)) 

    def testChecker_28(self):
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
        inp = Program([StructType("S1",[("EVA_01",IntType())],[]),StructType("S2",[("EVA_01",IntType())],[]),InterfaceType("I1",[Prototype("EVA_01",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("EVA_01",[IntType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("EVA_01",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        self.assertTrue(TestChecker.test(inp, "Redeclared Method: EVA_01\n",428))

    def testChecker_29(self):
        """
func foo(){
    if (true) {
         var a float = 1.02;
    } else {
        var a int = 1.02;
    }
}
        """
        inp = Program([FuncDecl("foo",[],VoidType(),Block([If(BooleanLiteral("true"), Block([VarDecl("a",FloatType(),FloatLiteral(1.02))]), Block([VarDecl("a",IntType(),FloatLiteral(1.02))]))]))])
        self.assertTrue(TestChecker.test(inp, "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.02))\n",429))

    def testChecker_30(self):
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
        inp = Program([FuncDecl("foo",[],VoidType(),Block([Return(None)])),FuncDecl("foo1",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo2",[],FloatType(),Block([Return(IntLiteral(2))]))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: Return(IntLiteral(2))\n""",430))

    def testChecker_31(self):
        """
var a = [2] int {1, 2}
var c [2] float = a
        """
        inp = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(2)],FloatType()),Id("a"))])
        self.assertTrue(TestChecker.test(inp, "",431))

    def testChecker_32(self):
        inp = """
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
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: VarDecl(e,IntType,FloatLiteral(6.0))\n""",432))

    def testChecker_33(self):
        """
var a boolean = true && false || true;
var b boolean = true && 1;
        """
        inp = Program([VarDecl("a",BoolType(),BinaryOp("||", BinaryOp("&&", BooleanLiteral("True"), BooleanLiteral("False")), BooleanLiteral("True"))),VarDecl("b",BoolType(),BinaryOp("&&", BooleanLiteral("True"), IntLiteral(1)))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: BinaryOp(BooleanLiteral(true),&&,IntLiteral(1))\n""",433))

    def testChecker_34(self):
        """
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
        """
        inp = Program([VarDecl("a",BoolType(),BinaryOp(">", IntLiteral(1), IntLiteral(2))),VarDecl("b",BoolType(),BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),VarDecl("c",BoolType(),BinaryOp("==", StringLiteral("""1"""), StringLiteral("""2"""))),VarDecl("d",BoolType(),BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: BinaryOp(IntLiteral(1),>,FloatLiteral(2.0))\n""",434))

    def testChecker_35(self):
        """
var a Replicant;
func foo() Replicant {
    return a;
    return Replicant;
}

type Replicant struct {Nosferatu int;}
        """
        inp =  Program([VarDecl("a",Id("Replicant"), None),FuncDecl("foo",[],Id("Replicant"),Block([Return(Id("a")),Return(Id("Replicant"))])),StructType("Replicant",[("Nosferatu",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, """Undeclared Identifier: Replicant\n""",435)) 

    def testChecker_36(self):
        """
type putLn struct {a int;};
        """
        inp = Program([StructType("putLn",[("a",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, """Redeclared Type: putLn\n""",436))

    def testChecker_37(self):
        """
type putLn interface {foo();};
        """
        inp = Program([InterfaceType("putLn",[Prototype("foo",[],VoidType())])])
        self.assertTrue(TestChecker.test(inp, """Redeclared Type: putLn\n""",437))

    def testChecker_38(self):
        """
var a int = getBool();
        """
        inp = Program([VarDecl("a",IntType(),FuncCall("getBool",[]))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: VarDecl(a,IntType,FuncCall(getBool,[]))\n""",438))

    def testChecker_39(self):
        """
func foo() {
    putFloat(getInt());
}
        """
        inp = Program([FuncDecl("foo",[],VoidType(),Block([FuncCall("putFloat",[FuncCall("getInt",[])])]))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: FuncCall(putFloat,[FuncCall(getInt,[])])\n""",439))

    def testChecker_40(self):
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
        inp = Program([FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,IntLiteral(1)),If(BinaryOp("<", Id("a"), IntLiteral(3)), Block([VarDecl("a", None,IntLiteral(1))]), If(BinaryOp(">", Id("a"), IntLiteral(2)), Block([VarDecl("a", None,IntLiteral(2))]), None)),Return(Id("a"))]))])
        self.assertTrue(TestChecker.test(inp, "",440))

    def testChecker_41(self):
        """
var A = 1;
type A struct {a int;}
        """
        inp =  Program([VarDecl("A", None,IntLiteral(1)),StructType("A",[("a",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, """Redeclared Type: A\n""",441)) 

    def testChecker_42(self):
        """
type S1 struct {EVA_01 int;}
type I1 interface {EVA_01();}

func (s S1) EVA_01() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        inp = Program([StructType("S1",[("EVA_01",IntType())],[]),InterfaceType("I1",[Prototype("EVA_01",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("EVA_01",[],VoidType(),Block([Return(None)]))),VarDecl("b",ArrayType([IntLiteral(2)],Id("S1")), None),VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))])
        self.assertTrue(TestChecker.test(inp, """Redeclared Method: EVA_01\n""",442)) 

    def testChecker_43(self):
        """
var a [10] int;
var b [10] int = a;
        """
        inp =  Program([VarDecl("a",ArrayType([IntLiteral(10)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(inp, """""",443)) 

    def testChecker_44(self):
        """
var a [10] int;
var b [10] int = a;
        """
        inp =  Program([VarDecl("a",ArrayType([IntLiteral(10)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(inp, """""",444)) 

    def testChecker_45(self):
        """
var a [2] int;
var b [5] int = a;
        """
        inp =  Program([VarDecl("a",ArrayType([IntLiteral(2)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(5)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: VarDecl(b,ArrayType(IntType,[IntLiteral(5)]),Id(a))\n""",445)) 

    def testChecker_46(self):
        """
var a [d] int;
var b [1] int = a;
        """
        inp =  Program([VarDecl("a",ArrayType([Id("d")],IntType()), None),VarDecl("b",ArrayType([IntLiteral(1)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(inp, """Undeclared Identifier: d\n""",446)) 

    def testChecker_47(self):
        inp = """
const a = 2 * 3;
var b [a] int;
var c [16] int = b;
        """
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: VarDecl(c,ArrayType(IntType,[IntLiteral(16)]),Id(b))\n""",447)) 

    def testChecker_48(self):
        inp = """
const v = 3;
const k = v - 1;
func foo(a [3] int) {
    foo([k] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: FuncCall(foo,[ArrayLiteral([Id(k)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])\n""",448))

    def testChecker_49(self):
        inp = """
type K struct {a int;}
func (k K) koo(a [3] int) {return;}
type H interface {koo(a [7] int);}

const c = 2 + 5;
func foo() {
    var k H;
    k.koo([7] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(inp, """""",449)) 

    def testChecker_50(self):
        """
const a = "2" + "#";
const b = a * 5;
        """
        inp =  Program([ConstDecl("a",None,BinaryOp("+", StringLiteral("""2"""), StringLiteral("""#"""))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5)))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: BinaryOp(Id(a),*,IntLiteral(5))\n""",450)) 

    def testChecker_51(self):
        inp = """
const v = 2 * 3;
const a = v + 1;
const b = a * 5;
const c = ! (b > 3);
var x [c] int = [0] int {3}
        """
        self.assertTrue(TestChecker.test(inp, "Type Mismatch: ArrayType(IntType,[Id(c)])\n",451)) 

    def testChecker_52(self):
        """
const a = 3;
const b = -a;
const c = -b;
var d [c] int = [3] int {1,2,3}
        """
        inp =  Program([ConstDecl("a",None,IntLiteral(3)),ConstDecl("b",None,UnaryOp("-",Id("a"))),ConstDecl("c",None,UnaryOp("-",Id("b"))),VarDecl("d",ArrayType([Id("c")],IntType()),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        self.assertTrue(TestChecker.test(inp, """""",452))

    def testChecker_53(self):
        """
func foo() {
    a := 1;
    var a = 1;
}
        """
        inp = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),IntLiteral(1)),VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(inp, """Redeclared Variable: a\n""",453)) 
    
    def testChecker_54(self):
        """
const a = 1;
func foo() {
    a := 1.;
}
        """
        inp = Program([ConstDecl("a",None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),FloatLiteral(1.0))]))])
        self.assertTrue(TestChecker.test(inp, """Type Mismatch: Assign(Id(a),FloatLiteral(1.0))\n""",454)) 

    def testChecker_55(self):
        """
func Ikari (b int) {
    for var a = 1; c < 1; a += c {
        const c = 2;
    }
}
        """
        inp = Program([FuncDecl("Ikari",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("c"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), Id("c"))),Block([ConstDecl("c",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(inp, """Undeclared Identifier: c\n""",455)) 

    def testChecker_56(self):
        """
var v Replicant;
func (v Replicant) foo (v int) int {
    return v;
}

type Replicant struct {
    Ikari int;
}
        """
        inp = Program([VarDecl("v",Id("Replicant"), None),MethodDecl("v",Id("Replicant"),FuncDecl("foo",[ParamDecl("v",IntType())],IntType(),Block([Return(Id("v"))]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, "",456))

    def testChecker_57(self):
        """
func (v Replicant) Ikari () {return ;}
type Replicant struct {
    Ikari int;
}
        """
        inp = Program([MethodDecl("v",Id("Replicant"),FuncDecl("Ikari",[],VoidType(),Block([Return(None)]))),StructType("Replicant",[("Ikari",IntType())],[])])
        self.assertTrue(TestChecker.test(inp, "Redeclared Method: Ikari\n",457))

    def testChecker_58(self):
        """
func foo() {
    foo := 1;
    foo()
}
        """
        inp = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("foo"),IntLiteral(1)),FuncCall("foo",[])]))])
        self.assertTrue(TestChecker.test(inp, "",458))

    def test_Checker_59(self):
        inp = \
            """func bar(arr float, b int) int{
var x [2][3] int
x[2][b] := bar(1.0,154/5)
var y int= getString()
}
"""
        out = """Type Mismatch: VarDecl(y,IntType,FuncCall(getString,[]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 459))

    def test_Checker_60(self):
        inp = \
            """const GREETING = "Hello, World!"

var message string

func main() {
    message := GREETING
    putString(message)
    var x boolean = 6.0
}
"""
        out = """Type Mismatch: VarDecl(x,BoolType,FloatLiteral(6.0))\n"""
        self.assertTrue(TestChecker.test(inp, out, 460))

    def test_Checker_61(self):
        inp = \
            """var a int = 10
var b float = 5
var result int

func main() {
    result := a + b*2 - b/2
    putIntLn(result)
}
"""
        out = "Type Mismatch: Assign(Id(result),BinaryOp(BinaryOp(Id(a),+,BinaryOp(Id(b),*,IntLiteral(2))),-,BinaryOp(Id(b),/,IntLiteral(2))))\n"
        self.assertTrue(TestChecker.test(inp, out, 461))

    def test_Checker_62(self):
        inp = \
            """var x int = 7

func main() {
    if (x > 5) {
        putString("x is greater than 5")
    } else {
        println("x is not greater than 5")
    }
}
"""
        out = """Undeclared Function: println\n"""
        self.assertTrue(TestChecker.test(inp, out, 462))

    def test_Checker_63(self):
        inp = \
            """var numbers [5]int = [5]int{1, 2, 3, 4, 5}

func main() {
    var value float;
    for _, value := range numbers {
        println(value)
    }
}
"""
        out = """Type Mismatch: ForEach(Id(_),Id(value),Id(numbers),Block([FuncCall(println,[Id(value)])]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 463))

    def test_Checker_64(self):
        inp = \
            """type Point struct {
    x int
    y int
}

var p Point

func main() {
    p.x := 10
    p.y := 20
    putIntLn(p.x)
    putIntLn(p.y)
    var t Point
    t.z := 9
}
"""
        out = "Undeclared Field: z\n"
        self.assertTrue(TestChecker.test(inp, out, 464))

    def test_Checker_65(self):
        inp = \
            """
type Printer interface {
    print(message string)
}

func main() {
    // No implementation here to test just declaration
    var x = main(5)
}

"""
        out = "Type Mismatch: FuncCall(main,[IntLiteral(5)])\n"
        self.assertTrue(TestChecker.test(inp, out, 465))

    def test_Checker_66(self):
        inp = \
            """type Rectangle struct {
    width int
    height int
}

func (r Rectangle) area() int {
    return r.width * r.height
}

var rect Rectangle

func main() {
    rect.width := 5
    rect.height := 10.0e+6
    putIntLn(rect.area())
}
"""
        out = """Type Mismatch: Assign(FieldAccess(Id(rect),height),FloatLiteral(10000000.0))\n"""
        self.assertTrue(TestChecker.test(inp, out, 466))

    def test_Checker_67(self):
        inp = \
            """func calculate(a int, b int) int {  // Invalid: Multiple return values
    return a + b
}

func main() {
    var sum int
    diff := calculate(10, 5)
    putIntLn(sum, diff)
}
"""
        out = "Type Mismatch: FuncCall(putIntLn,[Id(sum),Id(diff)])\n"
        self.assertTrue(TestChecker.test(inp, out, 467))

    def test_Checker_68(self):
        inp = \
            """var age int = 25
var isStudent boolean = false

func main() {
    if (age < 30) {
        if (!isStudent) {
            putStringLn("Young professional")
        } else {
            putStringLn("Young student")
        }
    } else {
        putInt([2]int{1, 2})
    }
}
"""
        out = """Type Mismatch: FuncCall(putInt,[ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)])])\n"""
        self.assertTrue(TestChecker.test(inp, out, 468))

    def test_Checker_69(self):
        inp = \
            """
func main() {
    for i := 0; i < 10; i += 1 {
        if (i % 3 == 0) {
            continue  // Skip multiples of 3
        }
        if (i > 7) {
            break     // Exit loop if i is greater than 7
        }
        var i = 4
    }
    break
}
"""
        out = """Redeclared Variable: i\n"""
        self.assertTrue(TestChecker.test(inp, out, 469))

    def test_Checker_70(self):
        inp = \
            """
type Circle struct {
    radius float
}

var circles [3]Circle

func main() {
    circles[0].radius := 5
    circles[1].radius := 7
    circles[2].radius := 9
    var c Circle
    for _, c := range circles {
        var x int
        putIntLn(x.radius)
    }
}
"""
        out = "Type Mismatch: FieldAccess(Id(x),radius)\n"
        self.assertTrue(TestChecker.test(inp, out, 470))

    def test_Checker_71(self):
        inp = \
            """func main() {
    for i:=0; i < 3; i+=1 {
        var j string
        for j != !false {
            putLn()
        }
    }
}"""
        out = "Type Mismatch: BinaryOp(Id(j),!=,UnaryOp(!,BooleanLiteral(false)))\n"
        self.assertTrue(TestChecker.test(inp, out, 471))

    def test_Checker_72(self):
        inp = \
            """/*
    This is a multi-line comment.
    It spans multiple lines.
*/
var x int = 10;

func main()  {
    putFloatLn(x) ;
}
"""
        out = "Type Mismatch: FuncCall(putFloatLn,[Id(x)])\n"
        self.assertTrue(TestChecker.test(inp, out, 472))

    def test_Checker_73(self):
        inp = \
            """var maxInt int = 2147483647  // Maximum 32-bit integer (adjust if needed)

func main() {
    var overflow int = maxInt + 1
    getInt()  //  What happens when we overflow?
}
"""
        out = "Type Mismatch: FuncCall(getInt,[])\n"
        self.assertTrue(TestChecker.test(inp, out, 473))

    def test_Checker_74(self):
        inp = \
            """ 
var message string = "This string contains a newline and a tab\t."

func main() {
    putString(message)
    var x boolean = 0
}
"""
        out = """Type Mismatch: VarDecl(x,BoolType,IntLiteral(0))\n"""
        self.assertTrue(TestChecker.test(inp, out, 474))

    def test_Checker_75(self):
        inp = \
            """ 
var x int = 5

func main(x int, y,z float, t [2][3]int, k boolean) {
    main(x,z,k,t,!k)
}
"""
        out = """Type Mismatch: FuncCall(main,[Id(x),Id(z),Id(k),Id(t),UnaryOp(!,Id(k))])\n"""
        self.assertTrue(TestChecker.test(inp, out, 475))

    def test_Checker_76(self):
        inp = \
            """var message string = "This string is not terminated"

func main() {
    var x string
    x := putString(message + "5")
}
"""
        out = """Type Mismatch: FuncCall(putString,[BinaryOp(Id(message),+,StringLiteral("5"))])\n"""
        self.assertTrue(TestChecker.test(inp, out, 476))

    def test_Checker_77(self):
        inp = \
            """ 
var x int = 5
var y int = 10 // /* */
func main() {
    putFloatLn(10 + 5)
}
"""
        out = "Type Mismatch: FuncCall(putFloatLn,[BinaryOp(IntLiteral(10),+,IntLiteral(5))])\n"
        self.assertTrue(TestChecker.test(inp, out, 477))

    def test_Checker_78(self):
        inp = \
            """ var x int = 5
type Person struct {
    x int
    y float
}
func main() {
    var x[1]float = Person{x: 5, y: 6.0} // x redeclared in the same scope
}
"""
        out = """Type Mismatch: VarDecl(x,ArrayType(FloatType,[IntLiteral(1)]),StructLiteral(Person,[(x,IntLiteral(5)),(y,FloatLiteral(6.0))]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 478))

    def test_Checker_79(self):
        inp = \
            """ var globalVar float = 20

func myFunction() {
    var localVar int = 10
    putFloatLn(globalVar + localVar)
}

func main() {
    myFunction()
    globalVar := 7
    putIntLn(localVar) // Error: localVar is not defined in main
}
"""
        out = """Undeclared Identifier: localVar\n"""
        self.assertTrue(TestChecker.test(inp, out, 479))

    def test_Checker_80(self):
        inp = \
            """ 
var a int = 10
var b int = 5
var c string = "hello"

func main() {
    if ((a > 5 && b < 10) || c == "world") {
        if (a + b == 3.e+3) {
            putStringLn("Condition met")
        } else {
            putStringLn("Inner condition failed")
        }
    } else {
        putStringLn("Outer condition failed")
    }
}
"""
        out = """Type Mismatch: BinaryOp(BinaryOp(Id(a),+,Id(b)),==,FloatLiteral(3000.0))\n"""
        self.assertTrue(TestChecker.test(inp, out, 480))

    def test_Checker_81(self):
        inp = \
            """var x int
var y int
var z int

func main() {
    x := 1
    y := 2 + 3
    z := 4 * 5 - 1
    println(x, y, z) // Illegal because it's not a function
}"""
        out = "Undeclared Function: println\n"
        self.assertTrue(TestChecker.test(inp, out, 481))

    def test_Checker_82(self):
        inp = \
            """func main() {
    for i := 0; i < 20; i+= 1 {
        if (i % 5 == 0) {
            continue // Skip multiples of 5
        }
        if (i > 3.E+5 && i < 15) {
            break    // Exit if between 13 and 14
        }
        putIntLn(i)
    }
}
"""
        out = """Type Mismatch: BinaryOp(Id(i),>,FloatLiteral(300000.0))\n"""
        self.assertTrue(TestChecker.test(inp, out, 482))

    def test_Checker_83(self):
        inp = \
            """type Person struct {
    name string
    age int
}

var p Person

func main() {
    p.name := "Alice"
    p.age := 11110 // Binary literal
    putString(p.name)
    var message string = p.name + " is " + p.age + " years old" // Concatenation with integer will cause a type error

}
"""
        out = """Type Mismatch: BinaryOp(BinaryOp(FieldAccess(Id(p),name),+,StringLiteral(" is ")),+,FieldAccess(Id(p),age))\n"""
        self.assertTrue(TestChecker.test(inp, out, 483))

    def test_Checker_84(self):
        inp = \
            """var data = [4]int{10, 20, 30, 40}

func main() {
    var index int
    var value int
    for index, value := range data {
        putIntLn(index * value)
    }
    data[index] := 6
    main(); y := 10
    var z int = y && true
}
"""
        out = "Type Mismatch: BinaryOp(Id(y),&&,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(inp, out, 484))

    def test_Checker_85(self):
        inp = \
            """
func findValue(arr [5]float, target float) int {
    for i := 0; i < 5; i+=1 {
        if (arr[i] == target) {
            return i // Return index if found
        }
    }
    return -1  // Return -1 if not found
}

var numbers [5]float = [5]int{1, 2, 3, 4, 5}

func main() {
    var index int = findValue(numbers, 3.0)
    return index
}
"""
        out = """Type Mismatch: Return(Id(index))\n"""
        self.assertTrue(TestChecker.test(inp, out, 485))

    def test_Checker_86(self):
        inp = \
            """var x int = 10
var y string = "hello"
var z boolean = true
const PI = 3.14

func main() {
    var y[PI]int
}
"""
        out = """Type Mismatch: ArrayType(IntType,[Id(PI)])\n"""
        self.assertTrue(TestChecker.test(inp, out, 486))

    def test_Checker_87(self):
        inp = \
            """type Address struct {
    street string
    city string
}

type Person struct {
    name string
    address Address
}

var p Person

func main() {
    p.name := "Bob"
    p.address.street := "123 Main St"
    p.address.city := "Anytown"
    p.address.state := "CA" // Error: state is not a field of Address
}
"""
        out = """Undeclared Field: state\n"""
        self.assertTrue(TestChecker.test(inp, out, 487))

    def test_Checker_88(self):
        inp = \
            """func isEven(n int) int {
    return (n + 1) % 2
}

var num int = 8

func main() {
    if (isEven(num)) {
        putStringLn("Even")
    } else {
        putStringLn("Odd")
    }
}
"""
        out = """Type Mismatch: If(FuncCall(isEven,[Id(num)]),Block([FuncCall(putStringLn,[StringLiteral("Even")])]),Block([FuncCall(putStringLn,[StringLiteral("Odd")])]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 488))

    def test_Checker_89(self):
        inp = \
            """var a int = 5
var b int = 69
var result boolean

func main() {
    result := a + b > 12 && a * b < 60
    putBool(result)
    putFloat(result)
}
"""
        out = """Type Mismatch: FuncCall(putFloat,[Id(result)])\n"""
        self.assertTrue(TestChecker.test(inp, out, 489))

    def test_Checker_90(self):
        inp = \
            """
func main() {
    for i := 0; i < 10; z/=2 { 
        putLn() 
    }
}
"""
        out = "Undeclared Identifier: z\n"
        self.assertTrue(TestChecker.test(inp, out, 490))

    def test_Checker_91(self):
        inp = \
            """
var x int = 10
const y = (7+6/4*5)%(7-2*1);
func main() {
    if (x > 5){
        putStringLn("x > 5")
    } else {
        putStringLn("x <= 5")
    }
}
var z [y] int = [3]int{1, 2, 3}
"""
        out = """Type Mismatch: VarDecl(z,ArrayType(IntType,[Id(y)]),ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 491))

    def test_Checker_92(self):
        inp = \
            """type MyInterface interface {
	doSomething()
}
type MyType struct{x MyInterface
}

func (m MyType) doSomething() {
	putStringLn("Hello")
}

func main() {
	var i MyInterface
	var m MyType
	i := m
    i.doSomething()// Calling method doSomething of MyInterface

    var y [5]MyInterface
    y[6].doSomething()
    y[6] := 10

}
"""
        out = """Type Mismatch: Assign(ArrayCell(Id(y),[IntLiteral(6)]),IntLiteral(10))\n"""
        self.assertTrue(TestChecker.test(inp, out, 492))

    def test_Checker_93(self):
        inp = \
            """
var a boolean = true
var b boolean = false
var c boolean = true

func main() int{
    var result boolean = (a && b) || (!c && a)
    return
}
"""
        out = """Type Mismatch: Return()\n"""
        self.assertTrue(TestChecker.test(inp, out, 493))

    def test_Checker_94(self):
        inp = \
            """
var numbers [3]int = [3]int{1, 2, 3}

func main() {
    var numbers [3]int = [4]int{0, 1, 2, 3}
}
"""
        out = """Type Mismatch: VarDecl(numbers,ArrayType(IntType,[IntLiteral(3)]),ArrayLiteral([IntLiteral(4)],IntType,[IntLiteral(0),IntLiteral(1),IntLiteral(2),IntLiteral(3)]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 494))

    def test_Checker_95(self):
        inp = \
            """var notAnArray int = 5;

func main() {
    var index int
    var value int
    for index, value := range notAnArray {
        index -= 1
    }
}
"""
        out = """Type Mismatch: ForEach(Id(index),Id(value),Id(notAnArray),Block([Assign(Id(index),BinaryOp(Id(index),-,IntLiteral(1)))]))\n"""
        self.assertTrue(TestChecker.test(inp, out, 495))

    def test_Checker_96(self):
        inp = \
            """func someOtherFunction() {
    putBool(8 == 5)
    someOtherFunction(8 == 5)
}
"""
        out = """Type Mismatch: FuncCall(someOtherFunction,[BinaryOp(IntLiteral(8),==,IntLiteral(5))])\n"""
        self.assertTrue(TestChecker.test(inp, out, 496))

    def test_Checker_97(self):
        inp = \
            """
        type Point struct {
            x int;
            y int;
        }
        type Circle struct {
            radius float;
            center Point;
        }
        func (c Circle) area() float {
            return 3.14 * c.radius * c.radius;
        }
        func main() {
            const circles = [3]Circle{
                Circle{radius: 1.0, center: Point{x: 0, y: 0}},
                Circle{radius: 2.0, center: Point{x: 1, y: 1}},
                Circle{radius: 3.0, center: Point{x: 2, y: 2, z: 3}} };
        }"""
        out = """Undeclared Field: z\n"""
        self.assertTrue(TestChecker.test(inp, out, 497))

    def test_Checker_98(self):
        inp = \
            """type MyType struct {
	Name string
}

func (mt MyType) someMethod() string {
	for i := 0; i < 10; i+=1 {
		if (i == 5) {
			return 5
		}
	}
	return "Not found"
}

func main() {
	mt := MyType{Name: "Example"}
	result := mt.someMethod()
	putStringLn(result)
}
"""
        out = """Type Mismatch: Return(IntLiteral(5))\n"""
        self.assertTrue(TestChecker.test(inp, out, 498))

    def test_Checker_99(self):
        """
        const a = [2][3]int{{1, 2, 3}, {4, 5, 6}};
        var b [2][3]int;
        func main() {
            var c [2][3]int = b;
            putFloatLn(c[1][2])
        }
"""
        inp = Program([ConstDecl("a",None,ArrayLiteral([IntLiteral(2),IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5),IntLiteral(6)])),VarDecl("b",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()),Id("a")),FuncDecl("main",[],VoidType(),Block([VarDecl("c",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()),Id("b")),FuncCall("putFloatLn",[ArrayCell(Id("c"),[IntLiteral(1),IntLiteral(2)])])]))])
        out = "Type Mismatch: FuncCall(putFloatLn,[ArrayCell(Id(c),[IntLiteral(1),IntLiteral(2)])])\n"
        self.assertTrue(TestChecker.test(inp, out, 499))