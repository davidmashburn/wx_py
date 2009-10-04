"""symbolConversion.py is a utility to support converting from unicode
symbols to an ascii format and vice-versa"""

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"

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

allSymbols = greek + GREEK

# Ordered names for Greek alphabets
greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
GREEK_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']

allNames = greek_names + GREEK_names
allExpandedAsciiNames = ['SYMPYSL_'+i+'_' for i in allNames]

operators = [unichr(i).encode('utf-8') for i in [0x000b7,0x02a2f]]
operator_names = ['dot', 'cross']

n2o = dict([[operator_names[i],operators[i]] for i in range(len(operators))])
o2n = dict([[operators[i],operator_names[i]] for i in range(len(operators))])

allOperators = operators
allExpandedAsciiOperatorNames = ['|Infix(numpy.'+i+')|' for i in operator_names]

# Dictionaries to convert from Greek names to Greek characters
n2g = dict([[greek_names[i],greek[i]] for i in range(24)])
N2G = dict([[GREEK_names[i],GREEK[i]] for i in range(24)])
# and vice-versa
g2n = dict([[greek[i],greek_names[i]] for i in range(24)])
G2N = dict([[GREEK[i],GREEK_names[i]] for i in range(24)])

# Dictionaries for "shorthand" conversion from 1 and 2 letter combinations to full Greek names
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
    for i in allOperators:
        if i in s:
            s = s.replace(i,'|Infix(numpy.'+Unicode2Ascii(i)+')|')
    
    return s.encode('ascii')

def FormatAsciiForDisplay(s): # s is an ascii string
    for i in allExpandedAsciiNames:
        if i in s:
            asciiName = i[8:-1]
            s = s.replace(i,Ascii2Unicode(asciiName))
    for i in allExpandedAsciiOperatorNames:
        if i in s:
            asciiName = i[13:-2]
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
