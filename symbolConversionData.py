## NEED TO FINISH MERGE WITHmathtextNamesSplitMergeWsC.py
# Maybe find a way to autoconvert this...

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

alpha2num = {
'a' : 0x61,
'b' : 0x62,
'c' : 0x63,
'd' : 0x64,
'e' : 0x65,
'f' : 0x66,
'g' : 0x67,
'h' : 0x68,
'i' : 0x69,
'j' : 0x6a,
'k' : 0x6b,
'l' : 0x6c,
'm' : 0x6d,
'n' : 0x6e,
'o' : 0x6f,
'p' : 0x70,
'q' : 0x71,
'r' : 0x72,
's' : 0x73,
't' : 0x74,
'u' : 0x75,
'v' : 0x76,
'w' : 0x77,
'x' : 0x78,
'y' : 0x79,
'z' : 0x7a
}

ALPHA2num = {
'A' : 0x41, 
'B' : 0x42,
'C' : 0x43,
'D' : 0x44,
'E' : 0x45,
'F' : 0x46,
'G' : 0x47,
'H' : 0x48,
'I' : 0x49,
'J' : 0x4a,
'K' : 0x4b,
'L' : 0x4c,
'M' : 0x4d,
'N' : 0x4e,
'O' : 0x4f,
'P' : 0x50,
'Q' : 0x51,
'R' : 0x52,
'S' : 0x53,
'T' : 0x54,
'U' : 0x55,
'V' : 0x56,
'W' : 0x57,
'X' : 0x58,
'Y' : 0x59,
'Z' : 0x5a
}

# character codes:
alpha = [chr(i) for i in alpha2num.values()]
ALPHA = [chr(i) for i in ALPHA2num.values()]

# ----- 3: Lowercase/UPPERCASE Greek alphabet -----

name2greek_Num = {
'alpha' : 0x3b1,
'beta' : 0x3b2,
'gamma' : 0x3b3,
'delta' : 0x3b4,
'epsilon' : 0x3f5, # lunate epsilon
'zeta' : 0x3b6,
'eta' : 0x3b7,
'theta' : 0x3b8,
'iota' : 0x3b9,
'kappa' : 0x3ba,
'lambda' : 0x3bb,
'mu' : 0x3bc,
'nu' : 0x3bd,
'xi' : 0x3be,
'omicron' : 0x3bf,
'pi' : 0x3c0,
'rho' : 0x3c1,
'sigma' : 0x3c3,
'tau' : 0x3c4,
'upsilon' : 0x3c5,
'phi' : 0x3d5, # 0x3c6 is now varphi (or cphi)
'chi' : 0x3c7,
'psi' : 0x3c8,
'omega' : 0x3c9,
'varepsilon' : 0x3b5, # curly epsilon
'varsigma' : 0x3c2, #finalsigma
'varphi' : 0x3c6,
'vartheta' : 0x3d1,
'varpi' : 0x3d6,
'digamma' : 0x3dd,
'varkappa' : 0x3f0,
'varrho' : 0x3f1,
'backepsilon' : 0x3f6,
}

name2GREEK_Num = {
'Alpha' : 0x391,
'Beta' : 0x392,
'Gamma' : 0x393,
'Delta' : 0x394,
'Epsilon' : 0x395,
'Zeta' : 0x396,
'Eta' : 0x397,
'Theta' : 0x398,
'Iota' : 0x399,
'Kappa' : 0x39a,
'Lambda' : 0x39b,
'Mu' : 0x39c,
'Nu' : 0x39d,
'Xi' : 0x39e,
'Omicron' : 0x39f,
'Pi' : 0x3a0,
'Rho' : 0x3a1,
'Sigma' : 0x3a3,
'Tau' : 0x3a4,
'Upsilon' : 0x3a5,
'Phi' : 0x3a6,
'Chi' : 0x3a7,
'Psi' : 0x3a8,
'Omega' : 0x3a9
}

# UTF-8 symbols:
greek=[unichr(i).encode('utf-8') for i in name2greek_Num.values()]
GREEK=[unichr(i).encode('utf-8') for i in name2GREEK_Num.values()]

# Ordered names for Greek alphabets:
greek_names = name2greek_Num.keys()
GREEK_names = name2GREEK_Num.keys()

# dict to convert from back and forth:
name2greek = dict([[greek_names[i],greek[i]] for i in range(len(greek))])
name2GREEK = dict([[GREEK_names[i],GREEK[i]] for i in range(len(GREEK))])
greek2name = dict([[greek[i],greek_names[i]] for i in range(len(greek))])
GREEK2name = dict([[GREEK[i],GREEK_names[i]] for i in range(len(GREEK))])

# dict's to convert single characters to full names
char2name = {
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

CHAR2name = {
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

name2greek['ce'] = name2greek['varepsilon']
name2greek['cph'] = name2greek['phi']
name2greek['cpi'] = name2greek['varpi']
name2greek['cth'] = name2greek['vartheta']
name2greek['ck'] = name2greek['varkappa']
name2greek['cr'] = name2greek['varrho']

name2greek['finalsigma'] = name2greek['varsigma']

name2GREEK['CH'] = name2GREEK['Chi']
name2GREEK['PH'] = name2GREEK['Phi']
name2GREEK['ET'] = name2GREEK['Eta']
name2GREEK['TH'] = name2GREEK['Theta']
name2GREEK['OM'] = name2GREEK['Omega']
name2GREEK['PS'] = name2GREEK['Psi']

# Symbols other than greek...
name2otherSymbols_Num = {
'ss' : 0xdf,
'eth' : 0xf0,
'hbar' : 0x127,
'dotlessi' : 0x131, #imath
'Lslash' : 0x141,
'lslash' : 0x142,
'OE' : 0x152,
'oe' : 0x153,
'Scaron' : 0x160,
'scaron' : 0x161,
'Ydieresis' : 0x178,
'Zcaron' : 0x17d,
'zcaron' : 0x17e,
'Agrave' : 0xc0,
'Aacute' : 0xc1,
'Acircumflex' : 0xc2,
'Atilde' : 0xc3,
'Adieresis' : 0xc4,
'Aring' : 0xc5,
'AE' : 0xc6,
'Ccedilla' : 0xc7,
'Egrave' : 0xc8,
'Eacute' : 0xc9,
'Ecircumflex' : 0xca,
'Edieresis' : 0xcb,
'Igrave' : 0xcc,
'Iacute' : 0xcd,
'Icircumflex' : 0xce,
'Idieresis' : 0xcf,
'Eth' : 0xd0,
'Ntilde' : 0xd1,
'Ograve' : 0xd2,
'Oacute' : 0xd3,
'Ocircumflex' : 0xd4,
'Otilde' : 0xd5,
'Odieresis' : 0xd6,
'Oslash' : 0xd8,
'Ugrave' : 0xd9,
'Uacute' : 0xda,
'Ucircumflex' : 0xdb,
'Udieresis' : 0xdc,
'Yacute' : 0xdd,
'Thorn' : 0xde,
'germandbls' : 0xdf,
'agrave' : 0xe0,
'aacute' : 0xe1,
'acircumflex' : 0xe2,
'atilde' : 0xe3,
'adieresis' : 0xe4,
'aring' : 0xe5,
'ae' : 0xe6,
'ccedilla' : 0xe7,
'egrave' : 0xe8,
'eacute' : 0xe9,
'ecircumflex' : 0xea,
'edieresis' : 0xeb,
'igrave' : 0xec,
'iacute' : 0xed,
'icircumflex' : 0xee,
'idieresis' : 0xef,
'eth' : 0xf0,
'ntilde' : 0xf1,
'ograve' : 0xf2,
'oacute' : 0xf3,
'ocircumflex' : 0xf4,
'otilde' : 0xf5,
'odieresis' : 0xf6,
'oslash' : 0xf8,
'ugrave' : 0xf9,
'uacute' : 0xfa,
'ucircumflex' : 0xfb,
'udieresis' : 0xfc,
'yacute' : 0xfd,
'thorn' : 0xfe,
'ydieresis' : 0xff,
'lambdabar' : 0x19b,
'BbbC' : 0x2102,
'scrg' : 0x210a,
'scrH' : 0x210b,
'hslash' : 0x210f,
'scrI' : 0x2110,
'Im' : 0x2111,
'scrL' : 0x2112,
'ell' : 0x2113,
'BbbN' : 0x2115,
'wp' : 0x2118,
'BbbP' : 0x2119,
'BbbQ' : 0x211a,
'scrR' : 0x211b,
'Re' : 0x211c,
'BbbR' : 0x211d,
'BbbZ' : 0x2124,
'mho' : 0x2127,
'frakZ' : 0x2128,
'AA' : 0x212b,
'scrB' : 0x212c,
'frakC' : 0x212d,
'scre' : 0x212f,
'scrE' : 0x2130,
'scrF' : 0x2131,
'Finv' : 0x2132,
'scrM' : 0x2133,
'scro' : 0x2134,
'aleph' : 0x2135,
'beth' : 0x2136,
'gimel' : 0x2137,
'daleth' : 0x2138,
'Game' : 0x2141
}

# ----- 4: Display only characters (mostly because I don't see how they -----
# ----- could be at all useful to convert these for the interpreter) -----
# Be warned, these will act like greek letters...
name2display_only_operator_Num = {
'upsidedownexclamation' : 0xa1,
'endofproof' : 0x220e,
'rightangle' : 0x221f,
'angle' : 0x2220,
'measuredangle' : 0x2221,
'sphericalangle' : 0x2222,
'therefore' : 0x2234,
'because' : 0x2235,
'ratio' : 0x2236,
'proportion' : 0x2237,
'sinewave' : 0x223f,
'cents' : 0xa2,
'pounds' : 0xa3,
'currency' : 0xa4,
'yen' : 0xa5,
'brokenbar' : 0xa6,
'copyright' : 0xa9,
'restricted' : 0xae,
'macron' : 0xaf,
'degree' : 0xb0,
'upsidedownquestion' : 0xbf
}

# UTF-8 symbols:
display_only_operators=[unichr(i).encode('utf-8') for i in name2display_only_operator_Num.values()]

# Ordered names for Greek alphabets:
display_only_operator_names = name2display_only_operator_Num.keys()

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
name2math_symbol_Num = {
'nullset' : 0x2205,
'infinity' : 0x221e
}

math_symbols=[unichr(i).encode('utf-8') for i in name2math_symbol_Num.values()]
math_symbol_names = name2math_symbol_Num.keys()

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
name2ez_operator_Num = {
'notequal' : 0x2260,
'lessthanequal' : 0x2264,
'greaterthanequal' : 0x2265,
'squared' : 0x00b2,
'cubed' : 0x00b3
}

ez_operators = [unichr(i).encode('utf-8') for i in name2ez_operator_Num.values()]
ez_operator_names = name2ez_operator_Num.keys()

name2ez_operator = dict([
                    [ez_operator_names[i],ez_operators[i]]
                    for i in range(len(ez_operators))
                        ])
ez_operator2name = dict([
                    [ez_operators[i],ez_operator_names[i]]
                    for i in range(len(ez_operators))
                        ])

ez_operator2interp = dict()
ez_operator2interp[name2ez_operator['notequal']] = '!='
ez_operator2interp[name2ez_operator['lessthanequal']] = '<='
ez_operator2interp[name2ez_operator['greaterthanequal']] = '>='
ez_operator2interp[name2ez_operator['squared']] = '**2'
ez_operator2interp[name2ez_operator['cubed']] = '**3'

name2ez_operator['!='] = name2ez_operator['notequal']
name2ez_operator['<='] = name2ez_operator['lessthanequal']
name2ez_operator['>='] = name2ez_operator['greaterthanequal']
name2ez_operator['^2'] = name2ez_operator['squared']
name2ez_operator['^3'] = name2ez_operator['cubed']
name2ez_operator['**2'] = name2ez_operator['squared']
name2ez_operator['**3'] = name2ez_operator['cubed']

# ----- 7: Prefix operators require parentheses like a function -----
name2prefix_operators_Num = {
'not' : 0xac,
'complement' : 0x2201,
'partial' : 0x2202,
'exists' : 0x2203,
'notexists' : 0x2204,
'increment' : 0x2206,
'nabla' : 0x2207,
'product' : 0x220f,
'coproduct' : 0x2210,
'summation' : 0x2211,
'squareroot' : 0x221a,
'cuberoot' : 0x221b,
'fourthroot' : 0x221c,
'integral' : 0x222b,
'doubleintegral' : 0x222c,
'tripleintegral' : 0x222d,
'contourintegral' : 0x222e,
'surfaceintegral' : 0x222f,
'volumeintegral' : 0x2230,
'clockwiseintegral' : 0x2231,
'clockwisecontourintegral' : 0x2232,
'counterclockwisecontourintegral' : 0x2233
}

prefix_operators = [unichr(i).encode('utf-8') for i in 
    name2prefix_operators_Num.values()]

prefix_operator_names = name2prefix_operators_Num.keys()

name2prefix_operator = dict([
                          [prefix_operator_names[i],prefix_operators[i]]
                          for i in range(len(prefix_operators))
                            ])
prefix_operator2name = dict([ 
                          [prefix_operators[i],prefix_operator_names[i]]
                          for i in range(len(prefix_operators))
                            ])

n2po = name2prefix_operator
n2po['neg']  = n2po['not']
n2po['logicalnot']  = n2po['not']
n2po['nexists']= n2po['notexists']
n2po['prod']   = n2po['product']
n2po['coprod'] = n2po['coproduct']
n2po['pd']   = n2po['partial']
n2po['del']  = n2po['nabla']
n2po['prod'] = n2po['product']
n2po['sum']  = n2po['summation']
n2po['sqrt'] = n2po['squareroot']
n2po['3rt']  = n2po['cuberoot']
n2po['4rt']  = n2po['fourthroot']
n2po['int']  = n2po['integral']
n2po['iint'] = n2po['doubleintegral']
n2po['iiint']= n2po['tripleintegral']
n2po['oint'] = n2po['contourintegral']
n2po['oiint']= n2po['surfaceintegral']
n2po['oiiint']= n2po['volumeintegral']
del n2po

# ----- 8: Binary (and Unary) Operators that need the special operator to function conversion -----
name2infix_binary_operator_Num = {
'plusminus' : 0xb1,
'divisionsign' : 0xf7,
'minusplus' : 0x2213,
'dotplus' : 0x2214,
'operatorminus' : 0x2212,
'forall' : 0x2200,
'divideoperator' : 0x2215,
'setminus' : 0x2216,
'elementof' : 0x2208,
'notelementof' : 0x2209,
'smallelementof' : 0x220a,
'contains' : 0x220b,
'notcontains' : 0x220c,
'smallcontains' : 0x220d,
'asterixoperator' : 0x2217,
'ring' : 0x2218,
'bullet' : 0x2219,
'proportional' : 0x221d,
'divides' : 0x2223,
'doesnotdivide' : 0x2224,
'parallel' : 0x2225,
'notparallel' : 0x2226,
'logicaland' : 0x2227,
'logicalor' : 0x2228,
'intersection' : 0x2229,
'union' : 0x222a,
'almostequal' : 0x2248,
'notalmostequal' : 0x2249,
'definedequal' : 0x225d,
'questionequal' : 0x225f,
'identicalto' : 0x2261,
'notidenticalto' : 0x2262,
'strictlyequivalentto' : 0x2263,
'muchless' : 0x226a,
'muchgreater' : 0x226b,
'subset' : 0x2282,
'superset' : 0x2283,
'notsubset' : 0x2284,
'notsuperset' : 0x2285,
'circleplus' : 0x2295,
'circleminus' : 0x2296,
'circletimes' : 0x2297,
'circledivide' : 0x2298,
'circledot' : 0x2299,
'circlering' : 0x229a,
'circleasterix' : 0x229b,
'circleequal' : 0x229c,
'circledash' : 0x229d,
'boxplus' : 0x229e,
'boxminus' : 0x229f,
'boxtimes' : 0x22a0,
'boxdot' : 0x22a1,
'diamond' : 0x22c4,
'dot' : 0x22c5,
'star' : 0x22c6,
'cross' : 0x2a2f
}

infix_binary_operators = [unichr(i).encode('utf-8') for i in 
                          name2infix_binary_operator_Num.values()]

infix_binary_operator_names = name2infix_binary_operator_Num.keys()

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

