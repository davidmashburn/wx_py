__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"
# 07/01/2009

import os
import glob

def pwd():
    print os.getcwd()

def cd(path,usePrint=True):
    os.chdir(os.path.expandvars(os.path.expanduser(path)))
    if usePrint:
        pwd()

def ls(str='*',fullpath=False):
    g=glob.glob(os.path.expandvars(os.path.expanduser(str)))
    if fullpath:
        for i in g:
            print i
    else:
        for i in g:
            print os.path.split(i)[1]

#cd('~',usePrint=False)
