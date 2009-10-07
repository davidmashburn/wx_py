"""symbolConversion.py is a utility to support converting from unicode
symbols to an ascii format and vice-versa"""

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"

import ast
from ast import Call, Load, Name, copy_location

nameAddOn = 'SYMPYSL_'

# Ok, this will work...
# First, build a list of all the BinOps left&right positions using a NodeVisitor
# Next, find the BinOp that has left<myop<right , but has right-left be a minimum
# Now, save THIS left-right pair to a list with the appropriate dictionary name for each operator
# and use this dictionary as the condition for matching operators (left,right == dict.leftright)
# Hooray, might work!
class BinOpRowColCollector(ast.NodeVisitor):
    def __init__(self):
        self.rowsCols = []
    
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.rowsCols .append([ [node.left.lineno, node.left.col_offset],
                                [node.right.lineno,node.right.col_offset] ])

class BinOp2Function(ast.NodeTransformer):
    def __init__(self):
        self.funcName = None
        self.astOp = None
        self.coords=[]
    def visit_BinOp(self, node):
        self.generic_visit(node)
        
        print node.op,node.left.col_offset,node.right.col_offset
        print node.left.lineno, node.left.col_offset,node.right.lineno,node.right.col_offset
        for c in self.coords:
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
        else:
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
                p = p.replace(nameAddOn+name+'_',n2precedence[name],1) # Take old ones out of the mix...
    return rowCol

def ASTWithConversion(s):
    names = operator_names
    rowCol = GetOperatorRowCol(s,names)
    for name in names:
        s = s.replace(nameAddOn+name+'_',n2precedence[name])
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
        bo2f.funcName = '__'+name+'__'
        bo2f.astOp = precedence2astName[n2precedence[name]]
        bo2f.coords=coords[name]
        mod = bo2f.visit(mod)
    return mod

# Symbol conversions from ascii to greek

ESC_SYMBOL = unichr(0x0022ee).encode('utf-8')

# Lowercase/UPPERCASE English alphabet (not used)
alpha=[chr(i) for i in range(97,97+26)]
ALPHA=[chr(i) for i in range(65,65+26)]

# Lowercase/UPPERCASE Greek alphabet
greek=[unichr(i).encode('utf-8') for i in range(0x003B1,0x003B1+25)]
GREEK=[unichr(i).encode('utf-8') for i in range(0x00391,0x00391+25)]
del(greek[17]) # Delete alternate form of sigma
del(GREEK[17]) # Delete empty character...

operators = [unichr(i).encode('utf-8') for i in [0x000b7,0x02a2f]]

allSymbols = greek + GREEK + operators

# Ordered names for Greek alphabets
greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
GREEK_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']

operator_names = ['dot', 'cross']
operatorSymbolForPrecedence = ['*','*']
# Dictionary to convert symbols to ast Names, in order of precedence
precedence2astName = {
'or' : ast.Or,
'and': ast.And,
'==' : ast.Eq,
'|'  : ast.BitOr,
'^'  : ast.BitXor,
'&'  : ast.BitAnd,
'<<' : ast.RShift,
'+'  : ast.Add,
'*'  : ast.Mult,
'**' : ast.Pow
}


allNames = greek_names + GREEK_names + operator_names
allExpandedAsciiNames = [nameAddOn + i + '_' for i in allNames]
expandedOperatorAsciiNames = [nameAddOn + i + '_' for i in operator_names]

# Operator Conversion dictionaries
n2o = dict([[operator_names[i],operators[i]] for i in range(len(operators))])
n2o['.']=n2o['dot']

o2n = dict([[operators[i],operator_names[i]] for i in range(len(operators))])
n2precedence = dict([[operator_names[i],operatorSymbolForPrecedence[i]] for i in range(len(operators))])

# Dictionaries to convert from Greek names to Greek characters
n2g = dict([[greek_names[i],greek[i]] for i in range(24)])
N2G = dict([[GREEK_names[i],GREEK[i]] for i in range(24)])
# and vice-versa
g2n = dict([[greek[i],greek_names[i]] for i in range(24)])
G2N = dict([[GREEK[i],GREEK_names[i]] for i in range(24)])

# Dictionaries for "shorthand" conversion from 1 and 2 letter combinations to full symbol names
a2n = {
'a' : 'alpha',
'b' : 'beta',
'c' : 'chi',
'd' : 'delta',
'e' : 'epsilon',
'f' : 'phi',
'g' : 'gamma',
'h' : 'eta',
'i' : 'iota',
'j' : 'phi',
'k' : 'kappa',
'l' : 'lambda',
'm' : 'mu',
'n' : 'nu',
'o' : 'omicron',
'p' : 'pi',
'q' : 'theta',
'r' : 'rho',
's' : 'sigma',
't' : 'tau',
'u' : 'upsilon',
'v' : 'nu',
'w' : 'omega',
'x' : 'xi',
'y' : 'psi',
'z' : 'zeta'
}

aa2n = {
'ch' : 'chi',
'ph' : 'phi',
'et' : 'eta',
'th' : 'theta',
'om' : 'omega',
'ps' : 'psi'
}

A2N = {
'A' : 'Alpha',
'B' : 'Beta',
'C' : 'Chi',
'D' : 'Delta',
'E' : 'Epsilon',
'F' : 'Phi',
'G' : 'Gamma',
'H' : 'Eta',
'I' : 'Iota',
'J' : 'Phi',
'K' : 'Kappa',
'L' : 'Lambda',
'M' : 'Mu',
'N' : 'Nu',
'O' : 'Omicron',
'P' : 'Pi',
'Q' : 'Theta',
'R' : 'Rho',
'S' : 'Sigma',
'T' : 'Tau',
'U' : 'Upsilon',
'V' : 'Nu',
'W' : 'Omega',
'X' : 'Xi',
'Y' : 'Psi',
'Z' : 'Zeta'
}

AA2N = {
'Ch' : 'Chi',
'Ph' : 'Phi',
'Et' : 'Eta',
'Th' : 'Theta',
'Om' : 'Omega',
'Ps' : 'Psi'
}

# Attempts to use the dictionaries above to convert ascii shorthand into a unicode character
def Ascii2Unicode(ascStr):
    if ascStr in n2g.keys():
        return n2g[ascStr]
    elif ascStr in N2G.keys():
        return N2G[ascStr]
    elif ascStr in a2n.keys():
        return n2g[a2n[ascStr]]
    elif ascStr in aa2n.keys():
        return n2g[aa2n[ascStr]]
    elif ascStr in A2N.keys():
        return N2G[A2N[ascStr]]
    elif ascStr in AA2N.keys():
        return N2G[AA2N[ascStr]]
    elif ascStr in n2o.keys():
        return n2o[ascStr]
    else:
        return ascStr

# Attempts to use the dictionaries above to return the ascii name of a unicode character
def Unicode2Ascii(uniChar):
    if uniChar == ESC_SYMBOL:
        print 'Error!  Unterminated Escape Charater!'
        return uniChr
    elif uniChar in greek:
        return g2n[uniChar]
    elif uniChar in GREEK:
        return G2N[uniChar]
    elif uniChar in operators:
        return o2n[uniChar]
    else:
        print 'Error!  Unrecognized Unicode Charater!'
        return hex(ord(uniChar))

def FormatUnicodeForPythonInterpreter(s): # s is a unicode string
    s = s.encode('utf-8')
    for i in allSymbols:
        if i in s:
            s = s.replace(i,'SYMPYSL_'+Unicode2Ascii(i)+'_')
    
    return s.encode('ascii')

def FormatAsciiForDisplay(s): # s is an ascii string
    for i in allExpandedAsciiNames:
        if i in s:
            asciiName = i[8:-1]
            s = s.replace(i,Ascii2Unicode(asciiName))
    
    return s
            

# point is to convert from unicode to ascii (and vice-versa) whether in SymPySlices or interpreter:
# unicode(0x003B1) <-> SYMPYSL_alpha_
# alternatively, could support wider range of unicode chars with:
# unicode(0x003B1) <-> SYMPYSL_03B1_
# but that is less human readable...
# I know!  Make that the default for anything that can't be id'd

# Need to add uppercase dicts, too

# other rather important operators
# sqrt, inf, e, integral, partial, I, differential, del, dot, cross, !=, <=, >=, +-, -+, <empty square>

# ?? other languages (hebrew, gothic, accent things, ...), other math notations, set notations, etc...

# layout operations (need MathML support):
# sqrt, matrix, super, sub, under, over, right of, left of, etc...


# the other big idea is to use NameError at the interpreter to attempt to resolve
# badSymbol by running badSymbol=sympy.symbols('badSymbol')
# but how to determine what symbol name is??
