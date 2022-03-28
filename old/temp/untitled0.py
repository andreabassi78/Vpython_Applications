# -*- coding: utf-8 -*-
"""
Created on Mon May 18 22:55:34 2020

@author: Andrea Bassi
"""
def decorator_func(x, y): 
  
    def Inner(func): 
  
        def wrapper(*args, **kwargs): 
            print("I like Geeksforgeeks") 
            print("Summation of values - {}".format(x+y) ) 
  
            func(*args, **kwargs) 
              
        return wrapper 
    return Inner 
  
  
@decorator_func(12,15) 
def my_fun(*args): 
    for ele in args: 
        print(ele) 
        
        
        
        
my_fun('Geeks', 'for', 'Geeks')