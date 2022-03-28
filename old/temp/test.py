# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:18:59 2020

@author: Andrea Bassi
"""

inner_called = False
print('ssfvdfv')
# decorator used to show multiple vectors as arrows in space,
# shown vectors are retured by "function" 


def inner(*args,**kwargs):
    vs = (0,5,6)#function(*args)
    sys = args[0]
    for index, v in enumerate(vs):
        if not inner_called: 
            print('yes')
            pass
    #inner_called = True
    #return vs

inner((0,1,2))    