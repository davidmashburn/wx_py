commands = """
import sympy

try:
    pass#import numpy as np
except:
    pass

try:
    if set==0: pass # stupid construct to avoid printing anything
except NameError:
    import sets.Set as set

SYMPYSL_Integral_ = sympy.integrate
SYMPYSL_NarySummation_ = sympy.sum
SYMPYSL_PartialDifferential_ = sympy.diff
SYMPYSL_Infinity_ = sympy.oo
SYMPYSL_GreekSmallLetterPi_ = sympy.pi
SYMPYSL_DoublestruckItalicSmallI_ = sympy.I
SYMPYSL_DoublestruckItalicSmallJ_ = sympy.I
SYMPYSL_DoublestruckItalicSmallE_ = sympy.E
SYMPYSL_SquareRoot_ = sympy.sqrt
SYMPYSL_CubeRoot_  = lambda x: x**(sympy.Rational(1,3))
SYMPYSL_FourthRoot_ = lambda x: x**(sympy.Rational(1,4))

def __Union__(x,y):
    return set(x).union(set(y))
    
def __Intersection__(x,y):
    return set(x).intersection(set(y))

def __FractionSlash__(x,y):
    if x.__class__ in [int,long,str] and \\
       y.__class__ in [int,long,str]:
        return sympy.Rational(x,y)
    else:
        return x/y

__DivisionSign__ = __FractionSlash__

def __DotOperator__(a,b):
    if a.__class__ == sympy.Matrix and b.__class__ == sympy.Matrix:
        return a.dot(a)
    elif hasattr(a,'__iter__') and hasattr(b,'__iter__'):
        doListVersion=True
        try:
            np
        except NameError:
            pass
        else:
            if hasattr(np,'__package__'):
                if np.__package__ == 'numpy':
                    doListVersion=False
        if doListVersion:
            return sum([a[i]*b[i] for i in range(len(a))])
        else:
            return np.dot(a,b)
    else:
        return sympy.Symbol('__DotOperator__')(a,b)
    
# Do this at the end...
from sympy import *
del(sum) # sum should be the standard sum function, not sympy sum...
"""
