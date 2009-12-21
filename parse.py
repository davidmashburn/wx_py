"""parse.py is a utility that allows simple checking for line continuations
to give the shell information about where text is commented and where it is
not and also how to appropriately break up a sequence of commands into
separate multi-line commands...
"""

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"
# created 12/20/2009

import re

# change this to testForContinuations

def testForContinuations(codeBlock):
    """ Test 4 different types of continuations:""" + \
    """ String Continuations (ie with ''')""" + \
    """ Indentation Block Continuations (ie "if 1:" )""" + \
    """ Line Continuations (ie with \\ character )""" + \
    """ Parenthetical continuations (, [, or {"""
    
    stringMark = None
    paraList = []
    
    stringMarks = ['"""',"'''",'"',"'"]
    openMarks = ['(','[','{']
    closeMarks = [')',']','}']
    paraMarkDict = { '(':')', '[':']', '{':'}' }
    
    stringContinuationList=[]
    lineContinuationList=[] # For \ continuations ... False because cannot start as line Continuation...
    indentationBlockList=[]
    parentheticalContinuationList=[]
    for i in codeBlock.split('\n'):
        firstWord = re.match(' *\w*','  for(5)6').group().lstrip()
        if firstWord in ['if','else','elif','for','while',
                         'def','class','try','except','finally']:
            hasContinuationWord = True
        else:
            hasContinuationWord = False
        
        
        result = re.finditer('"""'+'|'+"'''" + r'''|"|'|\"|\'|\(|\)|\[|\]|\{|\}|#''',i)
        
        commented=False
        
        nonCommentLength=len(i)
        
        for r in result:
            j = r.group()
            if stringMark == None:
                if j=='#': # If it is a legitimate comment, ignore everything after
                    commented=True
                    
                    # get length up to last non-comment character
                    nonCommentLength = r.start()
                    break
                elif j in stringMarks:
                    stringMark=j
                else:
                    if paraList != [] and j in closeMarks:
                        if paraMarkDict[paraList[-1]]==j:
                            paraList.pop()
                        else:
                            print 'Invalid Syntax!!'
                            # TODO: How to make this really call an error at the interpreter?
                            # Ahh... force it on into the interpreter do it creates an error!
                            # Maybe make this an option for shell mode...
                    if j in openMarks:
                        paraList.append(j)
            elif stringMark==j:
                stringMark=None
        
        stringContinuationList.append(stringMark!=None)
        
        indentationBlockList.append(False)
        
        nonCommentString = i[:nonCommentLength].rstrip()
        
        if nonCommentString!='':
            if nonCommentString[-1]==':':
                indentationBlockList[-1]=True
        
        lineContinuationList.append(False)
        if len(i)>0 and not commented:
            if i[-1]=='\\':
                lineContinuationList[-1]=True
        
        parentheticalContinuationList.append( paraList != [] )
    
    # Now stringContinuationList is line by line key for magic
    # telling it whether or not each next line is part of a string continuation
    
    return stringContinuationList,indentationBlockList,lineContinuationList,parentheticalContinuationList
