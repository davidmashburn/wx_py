commands = """
import numpy as np
try:
    if set==0:pass # stupid construct to avoid printing anything
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

def __DotOperator__(a, b):
    if a.__class__ == sympy.Matrix and b.__class__ == sympy.Matrix:
        return a.dot(a)
    elif hasattr(a,'__iter__') and hasattr(b,'__iter__'):
        return np.dot(a,b)
    else:
        return sympy.Symbol('__DotOperator__')(a,b)

from sympy import *


# alternative definitions
if 0:
    #import scipy.integrate
    SYMPYSL_sum_ = np.sum
    __DotOperator__ = np.dot
    SYMPYSL_pd_ = np.diff
    SYMPYSL_pi_ = np.pi
"""
