"""symbolConversion.py is a utility to support converting from unicode
symbols to an ascii format and vice-versa"""

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"

import ast
from ast import Call, Load, Name, copy_location
import unicodedata
from wx.py.symbolConversionDicts import infixOperatorNames, \
                                             NameToInfixAstSubstitute, \
                                          ToName, FromName,ToInterpreter
#from wx.py.symbolConversionData import *

nameAddOn = 'SYMPYSL_'

ESC_SYMBOL = unichr(0x0022ee).encode('utf-8')

# Strategy for conversion of Binary Operators to functions...
# 1 -- Replace the unicode character with one or another binary operator
#                                  (listed below in order of precedence)
# 2 -- Build a list of all the BinOps left&right positions using a NodeVisitor
# 3 -- Find the BinOp that has left<myop<right , but has right-left be a minimum
# 4 -- Save this left-right pair to a list with the appropriate dictionary
#                                                   name for each operator
# 5 -- Use this dictionary as the condition for matching operators
#                                         (left,right == dict.leftright)


# Dictionary to convert symbols to ast Names, in order of precedence
precedence2astName = {
'or' : ast.Or,
'and': ast.And,
'not' : ast.Not, # special for the not character (unary)
'==' : ast.Eq,
'|'  : ast.BitOr,
'^'  : ast.BitXor,
'&'  : ast.BitAnd,
'<<' : ast.RShift,
'+'  : ast.Add, # Can also be unary...
'*'  : ast.Mult,
'**' : ast.Pow
}

# add rules to deal with cases other than BinOp(expr left, operator op, expr right):
#1: BoolOp(boolop op, expr* values)
#2: Compare(expr left, cmpop* ops, expr* comparators)
#3: UnaryOp(unaryop op, expr operand)

# in the future, first test Unary Operators for replacement (to catch any quirks with +/-)
#   then do Compares, BoolOps and BinOps
# Note that Compares and BoolOps can be multiple...
#   this means that upon conversion, will have to change (==,or,and):
#        1 or 2 or 3
#     'Module(body=[Expr(value=BoolOp(op=Or(), values=[Num(n=1), Num(n=2), Num(n=3)]))])'
#   to:  (1 or 2) or 3
#     'Module(body=[Expr(value=BoolOp(op=Or(), values=[BoolOp(op=Or(), values=[Num(n=1), Num(n=2)]), Num(n=3)]))])'
#
#   and: 1 == 2 == 3
#     'Module(body=[Expr(value=Compare(left=Num(n=1), ops=[Eq(), Eq()], comparators=[Num(n=2), Num(n=3)]))])'
#   NOT TO:  (1 == 2) == 3
#     'Module(body=[Expr(value=Compare(left=Compare(left=Num(n=1), ops=[Eq()], comparators=[Num(n=2)]), ops=[Eq()], comparators=[Num(n=3)]))])'
#   but to:  1==2 and 2==3
#     'Module(body=[Expr(value=BoolOp(op=And(), values=[Compare(left=Num(n=1), ops=[Lt()], comparators=[Num(n=2)]),
#                                                       Compare(left=Num(n=2), ops=[Eq()], comparators=[Num(n=3)])]))])'

# Key ideas:
# If there are only 2 parameters, transform very much like BinOp, otherwise:
#  BoolOp has "op=Or()" and "values=[Num(n=1), Num(n=2), Num(n=3)]"
#  For BoolOp, convert to nested statements 1 or 2 or 3 -> f(f(1,2),3)
#  Compare has "left=Num(n=1)" and "ops=[Eq(), Eq()]" and "comparators=[Num(n=2), Num(n=3)]"
#  For Compare, first convert to and-separated statements: 1==2==3 -> 1==2 and 2==3
#  From there, convert to functions: 1==2 and 2==3 -> f(1,2) and f(2,3)

class BinOpRowColCollector(ast.NodeVisitor):
    def __init__(self):
        self.rowsCols = []
    
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.rowsCols.append([ [node.left.lineno, node.left.col_offset],
                               [node.right.lineno,node.right.col_offset] ])

class BinOp2Function(ast.NodeTransformer):
    def __init__(self):
        self.funcName = None
        self.astOp = None
        self.coords=[]
    def visit_BinOp(self, node):
        self.generic_visit(node)
        
        #print 'What is this??',node, '\nop', node.op,'\n',dir(node),'\nr',node.right,node.col_offset,node.lineno
        #print node.op,node.left.col_offset,node.right.col_offset
        #print node.left.lineno, node.left.col_offset,node.right.lineno,node.right.col_offset
        if self.coords != []:
            for c in self.coords:
                if len(c)!=0:
                    if node.left.lineno == c[0][0] and \
                       node.left.col_offset == c[0][1] and \
                       node.right.lineno == c[1][0] and \
                       node.right.col_offset == c[1][1]:
                        if self.astOp != type(node.op):
                            print 'Parsing Error!!'
                        print 'DONE!'
                        return copy_location(Call(
                                   func=Name(self.funcName, Load(),lineno=node.lineno,
                                             col_offset=node.col_offset),
                                   args=[node.left, node.right],
                                   keywords=[],
                                   lineno=node.lineno,
                                   col_offset=node.col_offset),
                               node)
        # If nothing changed, return as is...
        return node

def GetOperatorRowCol(s,names):
    rowCol = {}
    for name in names:
        rowCol[name] = []
    for row,p in enumerate(s.split('\n')):
        for name in names:
            while p.find(nameAddOn+name+'_') != -1:
                col = p.find(nameAddOn+name+'_')
                rowCol[name].append([row+1,p.find(nameAddOn+name+'_')])
                # Take old ones out of the mix...
                p = p.replace(nameAddOn+name+'_',NameToInfixAstSubstitute[name],1)
    return rowCol

def ASTWithConversion(s):
    names = infixOperatorNames
    rowCol = GetOperatorRowCol(s,names)
    for name in names:
        s = s.replace(nameAddOn+name+'_',NameToInfixAstSubstitute[name])
    print s
    mod=ast.parse(s,mode='single')
    borcc = BinOpRowColCollector()
    borcc.visit(mod)
    
    coords = {}
    
    for name in names:
        coords[name] = []
        for i,rc in enumerate(rowCol[name]):
            coords[name].append([]) # coords[name][i] = []
            for rl in borcc.rowsCols:
                # If rc is within rl...
                #  left.lineno          right.lineno
                #  left.col_offset    right.col_offset
                if rl[0][0] <= rc[0] <= rl[1][0] and \
                   rl[0][1] < rc[1] < rl[1][1]:
                    if coords[name][i] == []:
                        coords[name][i] = rl
                    # If this rl is tighter than coords[name][i]
                    elif rl[0][0] >= coords[name][i][0][0] and \
                         rl[0][1] >= coords[name][i][0][1] and \
                         rl[1][1] <= coords[name][i][0][1] and \
                         rl[1][1] <= coords[name][i][0][1]:
                        coords[name][i] = rl
    
    print coords
    bo2f=BinOp2Function()
    for name in names:
        if len(coords[name])>0:
            bo2f.funcName = '__'+ToName[FromName[name].decode('utf-8')]+'__'
            bo2f.astOp = precedence2astName[NameToInfixAstSubstitute[name]]
            bo2f.coords=coords[name]
            mod = bo2f.visit(mod)
    return mod

# ----------- Define Functions to convert characters and strings ---------

# Attempts to use the dictionaries in symbolConversionData to convert ascii shorthand into a unicode character
def Ascii2Unicode(ascStr):
    try:
        newStr = FromName[ascStr]
    except KeyError:
        newStr = ascStr
        print "name not found"
        pass
    
    return newStr

# Attempts to use the dictionaries in symbolConversionData to return the ascii name of a unicode character
def Unicode2Ascii(uniChar):
    if uniChar.encode('utf-8') == ESC_SYMBOL:
        print 'Error!  Unterminated Escape Charater!'
        return uniChar
    
    try:
        newStr = ToName[uniChar]
    except KeyError:
        newStr = uniChar
        print "name not found"
        pass
    
    return newStr

def Unicode2Ascii_Interp(uniChar):
    if uniChar.encode('utf-8') == ESC_SYMBOL:
        print 'Error!  Unterminated Escape Charater!'
        return uniChar
    
    try:
        newStr = ToInterpreter[uniChar]
    except KeyError:
        newStr = uniChar
        print "name not found"
        pass
    
    return newStr

def FormatUnicodeForSave(s): # s is a unicode string
    s = s.encode('utf-8')
    s = s.decode('utf-8')
    
    i=0
    while i<len(s):
        if ord(s[i])>=128:
            s = s.replace(s[i],nameAddOn+Unicode2Ascii(s[i])+'_')
        i+=1
    
    return s.encode('ascii')

def FormatUnicodeForPythonInterpreter(s): # s is a unicode string
    s = s.encode('utf-8')
    s = s.decode('utf-8')
    
    i=0
    while i<len(s):
        if ord(s[i])>=128:
            s = s.replace(s[i],Unicode2Ascii_Interp(s[i]))
        i+=1
    
    return s


def FormatAsciiForDisplay(s): # s is an ascii string
    for i in range(10000): # put a safety maxIterator in...
        start=s.find(nameAddOn)
        if start==-1:
            break
        end=start+len(nameAddOn)
        end = s[end:].find('_')+end+1
        asciiName = s[(start+len(nameAddOn)):(end-1)]
        s = s.replace(s[start:end],Ascii2Unicode(asciiName))
    
    return s

