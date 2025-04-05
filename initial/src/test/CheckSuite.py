import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    # def test_400(self):
    #     input = """var a int; var b int; var b int;"""
    #     expect = "Redeclared Variable: b\n"
    #     self.assertTrue(TestChecker.test(input,expect,400))

    # def test_401(self):
    #     input = """var a int = 1.2;"""
    #     expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.2))\n"
    #     self.assertTrue(TestChecker.test(input,expect,401))

    # def test_402(self):
    #     input = """var a int = b;"""
    #     expect = "Undeclared Identifier: b\n"
    #     self.assertTrue(TestChecker.test(input,expect,402))

    def test_403(self):
        input = """ // Test case 0: Basic program with simple arithmetic and output
const Point int = 6
func main() {
    var x int = 5;
    var y int = 10
    var result int = x + y * 2
    println(result);
}

 type Calculator interface {
 Add(x, y int) int;
 Subtract(a, b float, c int) float;
 Reset()
 SayHello(name string)
 }

func (e Calculator) Reset() {a := b;}
func (e Calculator) Reset() {c := b;}
"""
        expect = "Redeclared Method: Reset\n"
        self.assertTrue(TestChecker.test(input,expect,403))
  