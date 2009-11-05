"""symbolConversion.py is a utility to support converting from unicode
symbols to an ascii format and vice-versa"""

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"

import ast
from ast import Call, Load, Name, copy_location
import unicodedata
from newPyCrust.symbolConversionData import *

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
'not' : ast.Not, # special for the not character (unary)
'or' : ast.Or,
'and': ast.And,
'==' : ast.Eq,
'|'  : ast.BitOr,
'^'  : ast.BitXor,
'&'  : ast.BitAnd,
'<<' : ast.RShift,
'+'  : ast.Add, # Can also be unary...
'*'  : ast.Mult,
'**' : ast.Pow
}

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
                p = p.replace(nameAddOn+name+'_',
                    infix_binary_operator_name2precedence_symbol[name],1) # Take old ones out of the mix...
    return rowCol

def ASTWithConversion(s):
    names = infix_binary_operator_names
    rowCol = GetOperatorRowCol(s,names)
    for name in names:
        s = s.replace(nameAddOn+name+'_',infix_binary_operator_name2precedence_symbol[name])
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
            bo2f.funcName = '__'+name+'__'
            bo2f.astOp = precedence2astName[infix_binary_operator_name2precedence[name]]
            bo2f.coords=coords[name]
            mod = bo2f.visit(mod)
    return mod

# ----------- Define Functions to convert characters and strings ---------

# Attempts to use the dictionaries in symbolConversionData to convert ascii shorthand into a unicode character
def Ascii2Unicode(ascStr):
    for d in [name2greek, name2GREEK, name2display_only_operator,
              name2math_symbol, name2ez_operator,
              name2prefix_operator, name2infix_binary_operator]:
        if ascStr in d.keys():
            return d[ascStr]
    # if that didn't work, just return the ascii string back
    return ascStr

# Attempts to use the dictionaries in symbolConversionData to return the ascii name of a unicode character
def Unicode2Ascii(uniChar):
    if uniChar == ESC_SYMBOL:
        print 'Error!  Unterminated Escape Charater!'
        return uniChar
    
    for d in [greek2name, GREEK2name, display_only_operator2name,
              math_symbol2name, ez_operator2name,
              prefix_operator2name, infix_binary_operator2name]:
        if uniChar in d.keys():
            return d[uniChar]
    
    # Otherwise, this is an unrecognized char, so return the hex string instead...
    print 'Error!  Unrecognized Unicode Charater!'
    return hex(ord(uniChar))

def Unicode2Ascii_Interp(uniChar):
    for d in [ez_operator2interp]:
        if uniChar in d.keys():
            return d[uniChar]
    # No need to handle cases... check first before calling!

def FormatUnicodeForSave(s): # s is a unicode string
    s = s.encode('utf-8')
    
    for d in [greek2name, GREEK2name, display_only_operator2name,
              math_symbol2name, ez_operator2name,
              prefix_operator2name, infix_binary_operator2name]:
        for i in d.keys():
            if i in s:
                s = s.replace(i,nameAddOn+Unicode2Ascii(i)+'_')
    
    return s.encode('ascii')

def FormatUnicodeForPythonInterpreter(s): # s is a unicode string
    s = s.encode('utf-8')
    
    for d in [greek2name, GREEK2name, display_only_operator2name,
              math_symbol2name, infix_binary_operator2name]:
        for i in d.keys():
            if i in s:
                s = s.replace(i,nameAddOn+Unicode2Ascii(i)+'_')
    
    for d in [ez_operator2interp]:
        for i in d.keys():
            if i in s:
                s = s.replace(i,Unicode2Ascii_Interp(i))

    for i in prefix_operator2name.keys():
        if i in s:
            s = s.replace(i,'__'+Unicode2Ascii(i)+'__')
    
    return s.encode('ascii')

def FormatAsciiForDisplay(s): # s is an ascii string
    for i in allExpandedAsciiNames:
        if i in s:
            asciiName = i[len(nameAddOn):-1]
            s = s.replace(i,Ascii2Unicode(asciiName))
    
    return s
            
# Print all symbols and symbol names:
def PrintDocumentation():
    print """The purpose of this module is to convert from unicode to ascii
(and vice-versa) whether in SymPySlices or interpreter:
unicode(0x003B1) <-> SYMPYSL_alpha_
alternatively, could support wider range of unicode chars with:
unicode(0x003B1) <-> SYMPYSL_03B1_
but that is less human readable...
I know!  Make that the default for anything that can't be id'd
"""
    print 'Here is a list of all symbols defined, with their unicode number'
    print ', unicode name, and corresponding SymPySlices name:'
    
    print 'Lowercase Greek Letters:'
    for i in greek:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',greek2name[i]
    
    print '\nUppercase Greek Letters:'
    for i in GREEK:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',GREEK2name[i]
    
    print '\nCharacters for display only:'
    for i in display_only_operators:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',display_only_operator2name[i]
    
    print '\nMath Symbols:'
    for i in math_symbols:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',math_symbol2name[i], \
                                                      math_symbol2interp[i]
    
    print '\nEquality Operators:'
    ez_operator2name, ez_operator2interp
    for i in ez_operators:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',ez_operator2name[i], \
                                                      ez_operator2interp[i]
    
    print '\nPrefix Operators:'
    for i in prefix_operators:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',prefix_operator2name[i]
    
    print '\nInfix Operators:'
    for i in infix_binary_operators:
        print hex(ord(i.decode('utf-8'))),i,'', \
              unicodedata.name(i.decode('utf-8')),' ',infix_binary_operator2name[i]
    
# Need to add uppercase dicts, too

# other rather important operators
# sqrt, inf, e, integral, partial, I, differential, del, dot, cross, !=, <=, >=, +-, -+, <empty square>

# ?? other languages (hebrew, gothic, accent things, ...), other math notations, set notations, etc...

# layout operations (need MathML support):
# sqrt, matrix, super, sub, under, over, right of, left of, etc...


# the other big idea is to use NameError at the interpreter to attempt to resolve
# badSymbol by running badSymbol=sympy.symbols('badSymbol')
# but how to determine what symbol name is??

