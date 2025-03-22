import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
    lexerTest = 99
      
    ##### String-literal testcases #####
    def test_lexer_00(self):
        inp = """ "" """
        out = "\"\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_01(self):
        inp = """ "\n" """
        out = "Unclosed string: \""
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_02(self):
        inp = """ "white \&Glove"? """
        out = "Illegal escape in string: \"white \&"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_03(self):
        inp = """ "Gravity\tFalls\\n,<EOF>" """
        out = "\"Gravity\tFalls\\n,<EOF>\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_04(self):
        inp = """ "kanji'lang\\'8" """
        out = "Illegal escape in string: \"kanji'lang\\'"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_05(self):
        inp = """ "The Thing"! """
        out = "\"The Thing\",!,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_06(self):
        inp = """ "o.ri\\ga.mi" """
        out = "Illegal escape in string: \"o.ri\\g"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_07(self):
        inp = """ "Kaguya-Hime: '\"Love is Wrong?\"" """
        out = "\"Kaguya-Hime: '\",Love,is,Wrong,ErrorToken ?"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_08(self):
        inp = """ "dr.Watson\\r\\b  \\n\\t\\f' " """
        out = "Illegal escape in string: \"dr.Watson\\r\\b"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_09(self):
        inp = """ "Fate/destiny: \nHeaven\'s Hell" """
        out = "Unclosed string: \"Fate/destiny: "
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_10(self):
        inp = """ "2001'" """
        out = "\"2001'\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_11(self):
        inp = """ "akirA\\'" who?" """
        out = "Illegal escape in string: \"akirA\\'"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_12(self):
        inp = """ Carrie" """
        out = "Carrie,Unclosed string: \" "
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_13(self):
        inp = """ "soba,no,'\\\\fried ~!@#$%^&*()_+[;]" """
        out = "\"soba,no,'\\\\fried ~!@#$%^&*()_+[;]\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_14(self):
        inp = """ "oishi\' no\\ko" """
        out = "Illegal escape in string: \"oishi\' no\\k"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_15(self):
        inp = """ "Dark" Age'" """
        out = "\"Dark\",Age,ErrorToken '"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_16(self):
        inp = """ "814 + 94 + 343" """
        out = "\"814 + 94 + 343\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_17(self):
        inp = """ "func main() return 0" """
        out = "\"func main() return 0\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_18(self):
        inp = """ ""Shingeki==no" Kyojin" """
        out = "\"\",Shingeki,==,no,\" Kyojin\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_19(self):
        inp = """ "Fair^Gathering """
        out = "Unclosed string: \"Fair^Gathering "
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_20(self):
        inp = """ "Wuthering |Heights\"abc\"bb" """
        out = """\"Wuthering |Heights\",abc,\"bb\",<EOF>"""
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_21(self):
        inp = """ "'" """
        out = "\"'\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_22(self):
        inp = """ "{Lord<h>`<\\\\h>of the Rings}" """
        out = "\"{Lord<h>`<\\\\h>of the Rings}\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_23(self):
        inp = """ "Gatsby.\''no?" """
        out = "\"Gatsby.\''no?\",<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_24(self):
        inp = """ "''Moby Dick'''\\'" """
        out = "Illegal escape in string: \"''Moby Dick'''\\'"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    
    ##### Number-literal testcases #####

    def test_lexer_25(self):
        inp = "16"
        out = "16,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_26(self):
        inp = "-19586345612315798513321433092845743757437573974983433412315479797797977999133"
        out = "-,19586345612315798513321433092845743757437573974983433412315479797797977999133,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_27(self):
        inp = "61.45"
        out = "61.45,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_28(self):
        inp = "-1.4598e45625"
        out = "-,1.4598e45625,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_29(self):
        inp = "0.895e-16"
        out = "0.895e-16,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_30(self):
        inp = "2E-65"
        out = "2,E,-,65,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_31(self):
        inp = "0.e222967"
        out = "0.e222967,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_32(self):
        inp = ".E9632"
        out = ".,E9632,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_33(self):
        inp = "00001e279.003"
        out = "0,0,0,0,1,e279,.,0,0,3,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_34(self):
        inp = "000.00e+081"
        out = "000.00e+081,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_34(self):
        inp = "0"
        out = "0,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_35(self):
        inp = "41e"
        out = "41,e,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_36(self):
        inp = "19f-478"
        out = "19,f,-,478,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_37(self):
        inp = "41.3E2e-6"
        out = "41.3E2,e,-,6,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_38(self):
        inp = "e3223"
        out = "e3223,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_39(self):
        inp = "15.eE-61.8"
        out = "15.,eE,-,61.8,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))


    ##### Expression testcases #####

    def test_lexer_40(self):
        inp = "12 + 1 = 13"
        out = "12,+,1,=,13,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_41(self):
        inp = "21 + (31 =52 - x)"
        out = "21,+,(,31,=,52,-,x,),<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_42(self):
        inp = "24*\t7 +1 && true % int"
        out = "24,*,7,+,1,&&,true,%,int,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_43(self):
        inp = "x /true/\n2"
        out = "x,/,true,/,2,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_44(self):
        inp = "main ... \"method\" == main_method"
        out = "main,.,.,.,\"method\",==,main_method,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_45(self):
        inp = "x > \"y\" < z >= (t <= u) && v ! w"
        out = "x,>,\"y\",<,z,>=,(,t,<=,u,),&&,v,!,w,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_46(self):
        inp = "_h*i*j+45_"
        out = "_h,*,i,*,j,+,45,_,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_47(self):
        inp = "\t\n\n<<-- ! 7"
        out = "<,<,-,-,!,7,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_48(self):
        inp = "arr = arr[0][1] + time(x,const *9)"
        out = "arr,=,arr,[,0,],[,1,],+,time,(,x,,,const,*,9,),<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_49(self):
        inp = "1 + -2(\"var'\")nil"
        out = "1,+,-,2,(,\"var'\",),nil,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    ##### Syntax testcases #####

    def test_lexer_50(self):
        inp = \
            """ for i := 0; i < 10; i += 1 {
    if (x % i = 0) {return false;}
}
"""
        out = "for,i,:=,0,;,i,<,10,;,i,+=,1,{,if,(,x,%,i,=,0,),{,return,false,;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_51(self):
        inp = \
            """func main () {return 1;}

"""
        out = "func,main,(,),{,return,1,;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_52(self):
        inp = \
            """for i; i <= x / 2; i += 1
{
    if (x % i = 0) {return false
    }
}
"""
        out = "for,i,;,i,<=,x,/,2,;,i,+=,1,;,{,if,(,x,%,i,=,0,),{,return,false,;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_53(self):
        inp = \
            """func main(x string, y float)  {
}
"""
        out = "func,main,(,x,string,,,y,float,),{,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_54(self):
        inp = \
            """func foo(str string) boolean
writeString(str)
var x = 7 + (t - false)
"""
        out = "func,foo,(,str,string,),boolean,;,writeString,(,str,),;,var,x,=,7,+,(,t,-,false,),;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_55(self):
        inp = \
            """func bar( arr int,,){
x[2][8] := [3]{1,2,\"3\"} + [2]{4,\"5\",6}
}"""
        out = "func,bar,(,arr,int,,,,,),{,x,[,2,],[,8,],:=,[,3,],{,1,,,2,,,\"3\",},+,[,2,],{,4,,,\"5\",,,6,},;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_56(self):
        inp = \
            """
func min(int a, string b){  
if (x <= false){
        main(a,2,\"b\")
    }
for i; i <= x / 2; i += 1{ 

    loop1(arr[a(b)][b(a)])
    loop2(arr[a(b)],b[2])
}

}
"""
        out = "func,min,(,int,a,,,string,b,),{,if,(,x,<=,false,),{,main,(,a,,,2,,,\"b\",),;,},;,for,i,;,i,<=,x,/,2,;,i,+=,1,{,loop1,(,arr,[,a,(,b,),],[,b,(,a,),],),;,loop2,(,arr,[,a,(,b,),],,,b,[,2,],),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_57(self):
        inp = \
            """func min(a int, b string){ 
if (boolean) {
doSomething(a,2,\"b\");}
elif (abc > \"abc\") {doSomethingElif(b,true,foo(x,2))
}
else doSomethingElse(doSomethingElse,foo[3.2,3])
}

"""
        out = "func,min,(,a,int,,,b,string,),{,if,(,boolean,),{,doSomething,(,a,,,2,,,\"b\",),;,},;,elif,(,abc,>,\"abc\",),{,doSomethingElif,(,b,,,true,,,foo,(,x,,,2,),),;,},;,else,doSomethingElse,(,doSomethingElse,,,foo,[,3.2,,,3,],),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_58(self):
        inp = \
            """//func max(a int, b number)
/* begin
## Comment 1
##if (x == 6) else {doSomething();}
## Comment 2
*/
"""
        out = "<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_59(self):
        inp = \
            """func bar(arr float, b boolean) {
x[2][8] := foo(1,2,\"abcd\",154/4)
var x int= readString()"""
        out = "func,bar,(,arr,float,,,b,boolean,),{,x,[,2,],[,8,],:=,foo,(,1,,,2,,,\"abcd\",,,154,/,4,),;,var,x,int,=,readString,(,),<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_60(self):
        inp = \
            """const GREETING string = "Hello, World!"

var message string

func main() {
    message = GREETING
    println(message)
}
"""
        out = "const,GREETING,string,=,\"Hello, World!\",;,var,message,string,;,func,main,(,),{,message,=,GREETING,;,println,(,message,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_61(self):
        inp = \
            """var a int = 10
var b int = 5
var result int

func main() {
    result = a + b*2 - b/2
    println(result)
}
"""
        out = "var,a,int,=,10,;,var,b,int,=,5,;,var,result,int,;,func,main,(,),{,result,=,a,+,b,*,2,-,b,/,2,;,println,(,result,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_62(self):
        inp = \
            """var x int = 7

func main() {
    if (x > 5) {
        println("x is greater than 5")
    } else {
        println("x is not greater than 5")
    }
}
"""
        out = "var,x,int,=,7,;,func,main,(,),{,if,(,x,>,5,),{,println,(,\"x is greater than 5\",),;,},else,{,println,(,\"x is not greater than 5\",),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_63(self):
        inp = \
            """var numbers [5]int = [5]{1, 2, 3, 4, 5}

func main() {
    for index, value := range numbers {
        println(index, value)
    }
}
"""
        out = "var,numbers,[,5,],int,=,[,5,],{,1,,,2,,,3,,,4,,,5,},;,func,main,(,),{,for,index,,,value,:=,range,numbers,{,println,(,index,,,value,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_64(self):
        inp = \
            """type Point struct {
    x int
    y int
}

var p Point

func main() {
    p.x = 10
    p.y = 20
    println(p.x, p.y)
}"""
        out = "type,Point,struct,{,x,int,;,y,int,;,},;,var,p,Point,;,func,main,(,),{,p,.,x,=,10,;,p,.,y,=,20,;,println,(,p,.,x,,,p,.,y,),;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_65(self):
        inp = \
            """
type Printer interface {
    print(message string)
}

func main() {
    // No implementation here to test just declaration
}

"""
        out = "type,Printer,interface,{,print,(,message,string,),;,},;,func,main,(,),{,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_66(self):
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
    rect.width = 5
    rect.height = 10
    println(rect.area())
}
"""
        out = "type,Rectangle,struct,{,width,int,;,height,int,;,},;,func,(,r,Rectangle,),area,(,),int,{,return,r,.,width,*,r,.,height,;,},;,var,rect,Rectangle,;,func,main,(,),{,rect,.,width,=,5,;,rect,.,height,=,10,;,println,(,rect,.,area,(,),),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_67(self):
        inp = \
            """func calculate(a int, b int) (int, int) {  // Invalid: Multiple return values
    return a + b, a - b
}

func main() {
    var sum, diff int
    sum, diff = calculate(10, 5)
    println(sum, diff)
}
"""
        out = "func,calculate,(,a,int,,,b,int,),(,int,,,int,),{,return,a,+,b,,,a,-,b,;,},;,func,main,(,),{,var,sum,,,diff,int,;,sum,,,diff,=,calculate,(,10,,,5,),;,println,(,sum,,,diff,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_68(self):
        inp = \
            """var age int = 25
var isStudent bool = false

func main() {
    if (age < 30) {
        if (!isStudent) {
            println("Young professional")
        } else {
            println("Young student")
        }
    } else {
        println("Experienced")
    }
}
"""
        out = "var,age,int,=,25,;,var,isStudent,bool,=,false,;,func,main,(,),{,if,(,age,<,30,),{,if,(,!,isStudent,),{,println,(,\"Young professional\",),;,},else,{,println,(,\"Young student\",),;,},;,},else,{,println,(,\"Experienced\",),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_69(self):
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
        println(i)
    }
}
"""
        out = "func,main,(,),{,for,i,:=,0,;,i,<,10,;,i,+=,1,{,if,(,i,%,3,==,0,),{,continue,;,},;,if,(,i,>,7,),{,break,;,},;,println,(,i,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_70(self):
        inp = \
            """
type Circle struct {
    radius int
}

var circles [3]Circle

func main() {
    circles[0].radius = 5
    circles[1].radius = 7
    circles[2].radius = 9

    for _, c := range circles {
        println(c.radius)
    }
}
"""
        out = "type,Circle,struct,{,radius,int,;,},;,var,circles,[,3,],Circle,;,func,main,(,),{,circles,[,0,],.,radius,=,5,;,circles,[,1,],.,radius,=,7,;,circles,[,2,],.,radius,=,9,;,for,_,,,c,:=,range,circles,{,println,(,c,.,radius,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_71(self):
        inp = \
            """func main() {
    for i := 0; i < 3; i += 1 {
        for j := 0; j < 3; j += 1 {
            println(i, j)
        }
    }
}"""
        out = "func,main,(,),{,for,i,:=,0,;,i,<,3,;,i,+=,1,{,for,j,:=,0,;,j,<,3,;,j,+=,1,{,println,(,i,,,j,),;,},;,},;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_72(self):
        inp = \
            """/*
    This is a multi-line comment.
    It spans multiple lines.
*/

// This is a single-line comment.

var   x  int  =   10;  //  Declaration with extra whitespace

func main()  {
    //  More comments inside the function
    println ( x  ) ;
}"""
        out = "var,x,int,=,10,;,func,main,(,),{,println,(,x,),;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_73(self):
        inp = \
            """var maxInt int = 2147483647  // Maximum 32-bit integer (adjust if needed)

func main() {
    var overflow int = maxInt + 1
    println(overflow)  //  What happens when we overflow?
}
"""
        out = "var,maxInt,int,=,2147483647,;,func,main,(,),{,var,overflow,int,=,maxInt,+,1,;,println,(,overflow,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_74(self):
        inp = \
            """ 
var message string = "This string contains a newline\nand a tab\t."

func main() {
    println(message)
}
"""
        out = """var,message,string,=,Unclosed string: \"This string contains a newline"""
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_75(self):
        inp = \
            """ 
var x int = 5@  // Invalid character @

func main() {
    println(x)
}
"""
        out = "var,x,int,=,5,ErrorToken @"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_76(self):
        inp = \
            """var message string = "This string is not terminated

func main() {
    println(message)
}
"""
        out = """var,message,string,=,Unclosed string: "This string is not terminated"""
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_77(self):
        inp = \
            """ 
var x int = 5
var y int = 10 // Missing semicolon or newline here
func main() {
    println(x + y)
}
"""
        out = "var,x,int,=,5,;,var,y,int,=,10,;,func,main,(,),{,println,(,x,+,y,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_78(self):
        inp = \
            """ var x int = 5

func main() {
    var x string = "hello" // x redeclared in the same scope
    println(x)
}
"""
        out = "var,x,int,=,5,;,func,main,(,),{,var,x,string,=,\"hello\",;,println,(,x,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_79(self):
        inp = \
            """ var globalVar int = 20

func myFunction() {
    var localVar int = 10
    println(globalVar + localVar)
}

func main() {
    myFunction()
    println(globalVar) // Access global variable from main
    //println(localVar) // Error: localVar is not defined in main
}
"""
        out = "var,globalVar,int,=,20,;,func,myFunction,(,),{,var,localVar,int,=,10,;,println,(,globalVar,+,localVar,),;,},;,func,main,(,),{,myFunction,(,),;,println,(,globalVar,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_80(self):
        inp = \
            """ 
var a int = 10
var b int = 5
var c string = "hello"

func main() {
    if ((a > 5 && b < 10) || c == "world") {
        if (a + b == 15) {
            println("Condition met")
        } else {
            println("Inner condition failed")
        }
    } else {
        println("Outer condition failed")
    }
}
"""
        out = "var,a,int,=,10,;,var,b,int,=,5,;,var,c,string,=,\"hello\",;,func,main,(,),{,if,(,(,a,>,5,&&,b,<,10,),||,c,==,\"world\",),{,if,(,a,+,b,==,15,),{,println,(,\"Condition met\",),;,},else,{,println,(,\"Inner condition failed\",),;,},;,},else,{,println,(,\"Outer condition failed\",),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_81(self):
        inp = \
            """var x int
var y int
var z int

func main() {
    x, y, z = 1, 2 + 3, 4 * 5 - 1 // Note multi-assignment is illegal in MiniGo
    println(x, y, z) // Illegal because it's not a function
}"""
        out = "var,x,int,;,var,y,int,;,var,z,int,;,func,main,(,),{,x,,,y,,,z,=,1,,,2,+,3,,,4,*,5,-,1,;,println,(,x,,,y,,,z,),;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_82(self):
        inp = \
            """func main() {
    for i := 0; i < 20; i+= 1 {
        if (i % 5 == 0) {
            continue // Skip multiples of 5
        }
        if (i > 12 && i < 15) {
            break    // Exit if between 13 and 14
        }
        println(i)
    }
}"""
        out = "func,main,(,),{,for,i,:=,0,;,i,<,20,;,i,+=,1,{,if,(,i,%,5,==,0,),{,continue,;,},;,if,(,i,>,12,&&,i,<,15,),{,break,;,},;,println,(,i,),;,},;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_83(self):
        inp = \
            """type Person struct {
    name string
    age int
}

var p Person

func main() {
    p.name = "Alice"
    p.age = 30
    println(p.name, p.age)
    var message string = p.name + " is " + p.age + " years old" // Concatenation with integer will cause a type error

}
"""
        out = "type,Person,struct,{,name,string,;,age,int,;,},;,var,p,Person,;,func,main,(,),{,p,.,name,=,\"Alice\",;,p,.,age,=,30,;,println,(,p,.,name,,,p,.,age,),;,var,message,string,=,p,.,name,+,\" is \",+,p,.,age,+,\" years old\",;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_84(self):
        inp = \
            """var data [4]int = {10, 20, 30, 40}

func main() {
    for index, value := range data {
        println(index * value)
    }
    // data[index] =  // error: index not defined outside loop
}
"""
        out = "var,data,[,4,],int,=,{,10,,,20,,,30,,,40,},;,func,main,(,),{,for,index,,,value,:=,range,data,{,println,(,index,*,value,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_85(self):
        inp = \
            """
func findValue(arr [5]int, target int) int {
    for i := 0; i < 5; i+=1 {
        if (arr[i] == target) {
            return i // Return index if found
        }
    }
    return -1  // Return -1 if not found
}

var numbers [5]int = {1, 2, 3, 4, 5}

func main() {
    var index int = findValue(numbers, 3)
    println(index)
}
"""
        out = "func,findValue,(,arr,[,5,],int,,,target,int,),int,{,for,i,:=,0,;,i,<,5,;,i,+=,1,{,if,(,arr,[,i,],==,target,),{,return,i,;,},;,},;,return,-,1,;,},;,var,numbers,[,5,],int,=,{,1,,,2,,,3,,,4,,,5,},;,func,main,(,),{,var,index,int,=,findValue,(,numbers,,,3,),;,println,(,index,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_86(self):
        inp = \
            """var x int = 10
var y string = "hello"
var z bool = true
const PI float = 3.14

func main() {
    println(x, y, z, PI)
}
"""
        out = "var,x,int,=,10,;,var,y,string,=,\"hello\",;,var,z,bool,=,true,;,const,PI,float,=,3.14,;,func,main,(,),{,println,(,x,,,y,,,z,,,PI,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_87(self):
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
    p.name = "Bob"
    p.address.street = "123 Main St"
    p.address.city = "Anytown"
    println(p.name, p.address.street, p.address.city)
}
"""
        out = "type,Address,struct,{,street,string,;,city,string,;,},;,type,Person,struct,{,name,string,;,address,Address,;,},;,var,p,Person,;,func,main,(,),{,p,.,name,=,\"Bob\",;,p,.,address,.,street,=,\"123 Main St\",;,p,.,address,.,city,=,\"Anytown\",;,println,(,p,.,name,,,p,.,address,.,street,,,p,.,address,.,city,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_88(self):
        inp = \
            """func isEven(n int) bool {
    return n % 2 == 0
}

var num int = 8

func main() {
    if (isEven(num)) {
        println("Even")
    } else {
        println("Odd")
    }
}
"""
        out = "func,isEven,(,n,int,),bool,{,return,n,%,2,==,0,;,},;,var,num,int,=,8,;,func,main,(,),{,if,(,isEven,(,num,),),{,println,(,\"Even\",),;,},else,{,println,(,\"Odd\",),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_89(self):
        inp = \
            """var a int = 5
var b int = 10
var result bool

func main() {
    result = a + b > 12 && a * b < 60 // Will cause a type error because an int is compared to a bool
    println(result)
}
"""
        out = "var,a,int,=,5,;,var,b,int,=,10,;,var,result,bool,;,func,main,(,),{,result,=,a,+,b,>,12,&&,a,*,b,<,60,;,println,(,result,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_90(self):
        inp = \
            """
func main() {
    for i = 0; i < 10; i++ { 
        println(i) 
    }
}
"""
        out = "func,main,(,),{,for,i,=,0,;,i,<,10,;,i,+,+,{,println,(,i,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_91(self):
        inp = \
            """
var x int = 10

func main() {
    if (x > 5)
        println("x > 5")  // Missing braces - should cause an error
    else
        println("x <= 5")
}
"""
        out = "var,x,int,=,10,;,func,main,(,),{,if,(,x,>,5,),;,println,(,\"x > 5\",),;,else,println,(,\"x <= 5\",),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_92(self):
        inp = \
            """func main() {
    println(undefinedVariable) // Should cause error: undefinedVariable not declared
}
"""
        out = "func,main,(,),{,println,(,undefinedVariable,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_93(self):
        inp = \
            """func add(x int, y int) {  // Missing return type
    return x + y  // Type error
}

func main() {
   var result int = add(5,3)
   println(result)
}
"""
        out = "func,add,(,x,int,,,y,int,),{,return,x,+,y,;,},;,func,main,(,),{,var,result,int,=,add,(,5,,,3,),;,println,(,result,),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_94(self):
        inp = \
            """
var a bool = true
var b bool = false
var c bool = true

func main() {
    var result bool = (a && b) || (!c && a)
    println(result)
}"""
        out = "var,a,bool,=,true,;,var,b,bool,=,false,;,var,c,bool,=,true,;,func,main,(,),{,var,result,bool,=,(,a,&&,b,),||,(,!,c,&&,a,),;,println,(,result,),;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_95(self):
        inp = \
            """


var numbers [3]int = {1, "hello", 3} // "hello" is not an int. Error expected.

func main() {
    println(numbers[0], numbers[1], numbers[2])
}
"""
        out = "var,numbers,[,3,],int,=,{,1,,,\"hello\",,,3,},;,func,main,(,),{,println,(,numbers,[,0,],,,numbers,[,1,],,,numbers,[,2,],),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_96(self):
        inp = \
            """var notAnArray int = 5;

func main() {
    for index, value := range notAnArray {
        println(index, value);
    }
}
"""
        out = "var,notAnArray,int,=,5,;,func,main,(,),{,for,index,,,value,:=,range,notAnArray,{,println,(,index,,,value,),;,},;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_97(self):
        inp = \
            """func someOtherFunction() {
    println("This program does not have a main function")
}
"""
        out = "func,someOtherFunction,(,),{,println,(,\"This program does not have a main function\",),;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_98(self):
        inp = \
            """type MyInterface interface {
	doSomething()
}
type MyType struct{}

func (m MyType) doSomething() {
	println("Hello")
}

func main() {
	var i MyInterface
	var m MyType
	i = m

	//i.doSomething()// Calling method doSomething of MyInterface

}
"""
        out = "type,MyInterface,interface,{,doSomething,(,),;,},;,type,MyType,struct,{,},;,func,(,m,MyType,),doSomething,(,),{,println,(,\"Hello\",),;,},;,func,main,(,),{,var,i,MyInterface,;,var,m,MyType,;,i,=,m,;,},;,<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))

    def test_lexer_99(self):
        inp = \
            """type MyType struct {
	Name string
}

func (mt MyType) someMethod() string {
	for i := 0; i < 10; i++ {
		if i == 5 {
			return "Found 5!"
		}
	}
	return "Not found"
}

func main() {
	mt := MyType{Name: "Example"}
	result := mt.someMethod()
	println(result)
}"""
        out = "type,MyType,struct,{,Name,string,;,},;,func,(,mt,MyType,),someMethod,(,),string,{,for,i,:=,0,;,i,<,10,;,i,+,+,{,if,i,==,5,{,return,\"Found 5!\",;,},;,},;,return,\"Not found\",;,},;,func,main,(,),{,mt,:=,MyType,{,Name,:,\"Example\",},;,result,:=,mt,.,someMethod,(,),;,println,(,result,),;,},<EOF>"
        LexerSuite.lexerTest += 1
        self.assertTrue(TestLexer.checkLexeme(inp, out, LexerSuite.lexerTest))