import os

def Programming_Languages_Directory():
    PL_Directory  = os.getcwd() + '/Programming_Languages/'
    return PL_Directory

PL_Directory = Programming_Languages_Directory()

Path = []
Path.append(PL_Directory)
Path.append(os.getcwd() + '/Python_Scripts')
Path.append(PL_Directory + 'python/docplex')
Path.append(PL_Directory + 'cplex/python/3.7/x86-64_linux')

Python37_Directory = PL_Directory + 'python3.7'
# Python37_Directory = custom Python3.7 Path

Path.append(Python37_Directory)
Path.append(Python37_Directory + '/lib-dynload')
Path.append(Python37_Directory + '/site-packages')