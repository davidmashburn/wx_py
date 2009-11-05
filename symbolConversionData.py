nameAddOn = 'SYMPYSL_'

# -------------------------Unicode Conversion Dictionaries -------------------------
# There are 8 catagories of unicode conversions:
# 1:  ESC input character -- special case for help inputting unicode
# 2:  English alphabet (standard ascii...)
# 3:  Greek alphabet
# 4:  "Display Only" characters that seem nice but not particularly usable
# 5:  Mathematical symbols (infinity and the null set)
# 6:  Equality operators that can use simple substitution (!=,<=,>=)
# 7:  Prefix operators (integrals, summations, etc)
# 8:  Infix binary operators that require the AST replacement method (see above)

# -----  1: Special ellipsis character used for input method -----

# UTF-8 symbol
ESC_SYMBOL = unichr(0x0022ee).encode('utf-8')


# ----- 2: Lowercase/UPPERCASE English alphabet (not used) -----

# character codes:
alpha=[chr(i) for i in range(97,97+26)]
ALPHA=[chr(i) for i in range(65,65+26)]

# ----- 3: Lowercase/UPPERCASE Greek alphabet -----

# UTF-8 symbols:
greek=[unichr(i).encode('utf-8') for i in range(0x003B1,0x003B1+25)]
GREEK=[unichr(i).encode('utf-8') for i in range(0x00391,0x00391+25)]
del(greek[17]) # Delete alternate form of sigma
del(GREEK[17]) # Delete empty character...

# Ordered names for Greek alphabets:
greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
GREEK_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']

# dict's to convert back and forth:
name2greek = dict([[greek_names[i],greek[i]] for i in range(24)])
name2GREEK = dict([[GREEK_names[i],GREEK[i]] for i in range(24)])
greek2name = dict([[greek[i],greek_names[i]] for i in range(24)])
GREEK2name = dict([[GREEK[i],GREEK_names[i]] for i in range(24)])

# dict's to convert single characters to full names
char2name = { 'a' : 'alpha', 'b' : 'beta',    'c' : 'chi',
              'd' : 'delta', 'e' : 'epsilon', 'f' : 'phi',
              'g' : 'gamma', 'h' : 'eta',     'i' : 'iota',
              'j' : 'phi',   'k' : 'kappa',   'l' : 'lambda',
              'm' : 'mu',    'n' : 'nu',      'o' : 'omicron',
              'p' : 'pi',    'q' : 'theta',   'r' : 'rho',
              's' : 'sigma', 't' : 'tau',     'u' : 'upsilon',
              'v' : 'nu',    'w' : 'omega',   'x' : 'xi',
              'y' : 'psi',   'z' : 'zeta' }

CHAR2name = { 'A' : 'Alpha', 'B' : 'Beta',    'C' : 'Chi',
              'D' : 'Delta', 'E' : 'Epsilon', 'F' : 'Phi',
              'G' : 'Gamma', 'H' : 'Eta',     'I' : 'Iota',
              'J' : 'Phi',   'K' : 'Kappa',   'L' : 'Lambda',
              'M' : 'Mu',    'N' : 'Nu',      'O' : 'Omicron',
              'P' : 'Pi',    'Q' : 'Theta',   'R' : 'Rho',
              'S' : 'Sigma', 'T' : 'Tau',     'U' : 'Upsilon',
              'V' : 'Nu',    'W' : 'Omega',   'X' : 'Xi',
              'Y' : 'Psi',   'Z' : 'Zeta' }

# Add the single-character stuff to the name2greek/name2GREEK) dictionaries
for i in char2name.keys():
    name2greek[i] = name2greek[char2name[i]]

for i in CHAR2name.keys():
    name2GREEK[i] = name2GREEK[CHAR2name[i]]

name2greek['ch'] = name2greek['chi']
name2greek['ph'] = name2greek['phi']
name2greek['et'] = name2greek['eta']
name2greek['th'] = name2greek['theta']
name2greek['om'] = name2greek['omega']
name2greek['ps'] = name2greek['psi']

name2GREEK['CH'] = name2GREEK['Chi']
name2GREEK['PH'] = name2GREEK['Phi']
name2GREEK['ET'] = name2GREEK['Eta']
name2GREEK['TH'] = name2GREEK['Theta']
name2GREEK['OM'] = name2GREEK['Omega']
name2GREEK['PS'] = name2GREEK['Psi']

# ----- 4: Display only characters (mostly because I don't see how they -----
# ----- could be at all useful to convert these for the interpreter) -----
# Be warned, these will act like greek letters...
display_only_operators = [unichr(i).encode('utf-8') for i in
    [0x00a1, 0x220e, 0x221f, 0x2220, 0x2221, 0x2222, 0x2234, 0x2235,
     0x2236, 0x2237, 0x223f, 0x00a2, 0x00a3, 0x00a4, 0x00a5, 0x00a6,
     0x00a9, 0x00ae, 0x00af, 0x00b0, 0x00bf]]
display_only_operator_names = ['upsidedownexclamation','endofproof',
                               'rightangle','angle','measuredangle',
                               'sphericalangle','therefore','because',
                               'ratio','proportion','sinewave',
                               'cents','pounds','currency','yen',
                               'brokenbar','copyright',
                               'restricted','macron','degree',
                               'upsidedownquestion'
                              ]

name2display_only_operator = dict([
              [display_only_operator_names[i],display_only_operators[i]]
              for i in range(len(display_only_operators))
                                  ])
display_only_operator2name = dict([
              [display_only_operators[i],display_only_operator_names[i]]
              for i in range(len(display_only_operators))
                                  ])

n2doo = name2display_only_operator
n2doo['deg']  = n2doo['degree']
del n2doo

# ---- 5: Mathematical Symbols (Converts like greek) -----
math_symbols = [unichr(i).encode('utf-8') for i in [0x2205,0x221e]]
math_symbol_names = ['nullset','infinity']

name2math_symbol = dict([ [math_symbol_names[i],math_symbols[i]]
                          for i in range(len(math_symbols))
                        ])
math_symbol2name = dict([ [math_symbols[i],math_symbol_names[i]]
                          for i in range(len(math_symbols))
                        ])
#math_symbol2interp = dict([ [math_symbols[i],['sets.Set([])','sympy.oo'][i]]
#                             for i in range(len(math_symbols))
#                          ])

name2math_symbol['inf'] = name2math_symbol['infinity']

# ----- 6: Binary operators that support simple unicode to ascii conversion -----
# (all these are simple equality operators)
ez_operators = [unichr(i).encode('utf-8') for i in [0x2260, 0x2264, 0x2265, 0x00b2, 0x00b3]]
ez_operator_names = ['notequal','lessthanequal','greaterthanequal','squared','cubed']

name2ez_operator = dict([
                    [ez_operator_names[i],ez_operators[i]]
                    for i in range(len(ez_operators))
                               ])
ez_operator2name = dict([
                    [ez_operators[i],ez_operator_names[i]]
                    for i in range(len(ez_operators))
                               ])
ez_operator2interp = dict([
                               [ez_operators[i],['!=','<=','>=','**2','**3'][i]]
                               for i in range(len(ez_operators))
                                 ])

name2ez_operator['!='] = name2ez_operator['notequal']
name2ez_operator['<='] = name2ez_operator['lessthanequal']
name2ez_operator['>='] = name2ez_operator['greaterthanequal']
name2ez_operator['^2'] = name2ez_operator['squared']
name2ez_operator['^3'] = name2ez_operator['cubed']

# ----- 7: Prefix operators require parentheses like a function -----
prefix_operators = [unichr(i).encode('utf-8') for i in 
    [0x2201, 0x2202, 0x2203, 0x2204, 0x2206, 0x2207, 0x220f, 0x2210,
     0x2211, 0x221a, 0x221b, 0x221c, 0x222b, 0x222c, 0x222d, 0x222e,
     0x222f, 0x2230, 0x2231, 0x2232, 0x2233]]

prefix_operator_names = ['complement','partial','exists','notexists',
                          'increment','nabla','product','coproduct',
                          'summation','squareroot','cuberoot',
                          'fourthroot','integral','doubleintegral',
                          'tripleintegral','contourintegral',
                          'surfaceintegral','volumeintegral',
                          'clockwiseintegral','clockwisecontourintegral',
                          'counterclockwisecontourintegral']

name2prefix_operator = dict([
                          [prefix_operator_names[i],prefix_operators[i]]
                          for i in range(len(prefix_operators))
                            ])
prefix_operator2name = dict([ 
                          [prefix_operators[i],prefix_operator_names[i]]
                          for i in range(len(prefix_operators))
                            ])

n2po = name2prefix_operator
n2po['pd']   = n2po['partial']
n2po['del']  = n2po['nabla']
n2po['prod'] = n2po['product']
n2po['sum']  = n2po['summation']
n2po['sqrt'] = n2po['squareroot']
n2po['3rt']  = n2po['cuberoot']
n2po['4rt']  = n2po['fourthroot']
n2po['int']  = n2po['integral']
del n2po

# ----- 8: Binary (and Unary) Operators that need the special operator to function conversion -----
infix_binary_operators = [unichr(i).encode('utf-8') for i in 
    [0x00ac, 0x00b1, 0x00f7, 0x2213, 0x2214, 0x2212, 0x2200, 0x2215,
     0x2216, 0x2208, 0x2209, 0x220a, 0x220b, 0x220c, 0x220d, 0x2217,
     0x2218, 0x2219, 0x221d, 0x2223, 0x2224, 0x2225, 0x2226, 0x2227,
     0x2228, 0x2229, 0x222a, 0x2248, 0x2249, 0x225d, 0x225f, 0x2261,
     0x2262, 0x2263, 0x226a, 0x226b, 0x2282, 0x2283, 0x2284, 0x2285,
     0x2295, 0x2296, 0x2297, 0x2298, 0x2299, 0x229a, 0x229b, 0x229c,
     0x229d, 0x229e, 0x229f, 0x22a0, 0x22a1, 0x22c4, 0x22c5, 0x22c6,
     0x2a2f]]

infix_binary_operator_names = ['not','plusminus','divisionsign','minusplus',
                               'dotplus','operatorminus','forall',
                               'divideoperator','setminus','elementof',
                               'notelementof','smallelementof','contains',
                               'notcontains','smallcontains',
                               'asterixoperator','ring','bullet',
                               'proportional','divides','doesnotdivide',
                               'parallel','notparallel','logicaland',
                               'logicalor','intersection','union',
                               'almostequal','notalmostequal',
                               'definedequal','questionequal',
                               'identicalto','notidenticalto',
                               'strictlyequivalentto','muchless',
                               'muchgreater','subset','superset',
                               'notsubset', 'notsuperset','circleplus',
                               'circleminus','circletimes','circledivide',
                               'circledot','circlering','circleasterix',
                               'circleequal','circledash',
                               'boxplus','boxminus','boxtimes','boxdot',
                               'diamond','dot','star','cross'
                              ]

name2infix_binary_operator = dict([
              [infix_binary_operator_names[i],infix_binary_operators[i]]
              for i in range(len(infix_binary_operators))
                                  ])
infix_binary_operator2name = dict([
              [infix_binary_operators[i],infix_binary_operator_names[i]]
              for i in range(len(infix_binary_operators))
                                  ])

n2ibo = name2infix_binary_operator
n2ibo['/'] = n2ibo['divisionsign']
n2ibo['frac'] = n2ibo['divisionsign']
n2ibo['+-'] = n2ibo['plusminus']
n2ibo['-+'] = n2ibo['minusplus']
n2ibo['.+'] = n2ibo['dotplus']
n2ibo['prop'] = n2ibo['proportional']
n2ibo['para'] = n2ibo['parallel']
n2ibo['~~']   = n2ibo['almostequal']
n2ibo['!~~']  = n2ibo['notalmostequal']
n2ibo['def='] = n2ibo['definedequal']
n2ibo['?=']   = n2ibo['questionequal']
n2ibo['==='] = n2ibo['identicalto']
n2ibo['!==='] = n2ibo['notidenticalto']
n2ibo['===='] = n2ibo['strictlyequivalentto']
n2ibo['<<'] = n2ibo['muchless']
n2ibo['>>'] = n2ibo['muchgreater']
n2ibo['c+'] = n2ibo['circleplus']
n2ibo['c-'] = n2ibo['circleminus']
n2ibo['c*'] = n2ibo['circletimes']
n2ibo['c/'] = n2ibo['circledivide']
n2ibo['c.'] = n2ibo['circledot']
n2ibo['c='] = n2ibo['circleequal']
n2ibo['b+'] = n2ibo['boxplus']
n2ibo['b-'] = n2ibo['boxminus']
n2ibo['b*'] = n2ibo['boxtimes']
n2ibo['b.'] = n2ibo['boxdot']
n2ibo['dia'] = n2ibo['diamond']
n2ibo['.'] = n2ibo['dot'] # Don't use middledot anymore...
del n2ibo

infix_binary_operator_name2precedence_symbol = {
'not'                   : 'not',
'plusminus'             : '+',
'divisionsign'          : '*',
'minusplus'             : '+',
'dotplus'               : '*',
'operatorminus'         : '+',
'forall'                : 'or',
'divideoperator'        : '*',
'setminus'              : '*',
'elementof'             : '==',
'notelementof'          : '==',
'smallelementof'        : '==',
'contains'              : '==',
'notcontains'           : '==',
'smallcontains'         : '==',
'asterixoperator'       : '*',
'ring'                  : '*',
'bullet'                : '*',
'proportional'          : '==',
'divides'               : '==',
'doesnotdivide'         : '==',
'parallel'              : '==',
'notparallel'           : '==',
'logicaland'            : 'and',
'logicalor'             : 'or',
'intersection'          : 'and',
'union'                 : 'or',
'almostequal'           : '==',
'notalmostequal'        : '==',
'definedequal'          : '==',
'questionequal'         : '==',
'identicalto'           : '==',
'notidenticalto'        : '==',
'strictlyequivalentto'  : '==',
'muchless'              : '==',
'muchgreater'           : '==',
'subset'                : '==',
'superset'              : '==',
'notsubset'             : '==', 
'notsuperset'           : '==',
'circleplus'            : '*',
'circleminus'           : '*',
'circletimes'           : '*',
'circledivide'          : '*',
'circledot'             : '*',
'circlering'            : '*',
'circleasterix'         : '*',
'circleequal'           : '*',
'circledash'            : '*',
'boxplus'               : '*',
'boxminus'              : '*',
'boxtimes'              : '*',
'boxdot'                : '*',
'diamond'               : '*',
'dot'                   : '*',
'star'                  : '*',
'cross'                 : '*',
}

# --------------- Define allSymbols and allNames -----------------------

allSymbols = [ESC_SYMBOL] + greek + GREEK + display_only_operators
allSymbols += math_symbols + ez_operators + prefix_operators
allSymbols += infix_binary_operators

# This is used to convert 
allNames = greek_names + GREEK_names + display_only_operator_names
allNames += math_symbol_names + ez_operator_names
allNames += prefix_operator_names + infix_binary_operator_names

allExpandedAsciiNames = [nameAddOn + i + '_' for i in allNames]
expandedInfixOperatorAsciiNames = [nameAddOn + i + '_' for i in infix_binary_operator_names]

infix_binary_operator_name2precedence = {}

for i in infix_binary_operator_names:
    infix_binary_operator_name2precedence[i] = \
                       infix_binary_operator_name2precedence_symbol[i]
