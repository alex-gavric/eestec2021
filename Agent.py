from random import randint
import os
import importlib

def list_of_modules():
    modules = [f for f in os.listdir('.') if os.path.isfile(f)]        
    modules = [f[7:-3] for f in modules if f.startswith('module_') and f.endswith('.py')]        
    return modules

def list_of_objects():
    ret = []
    for module in list_of_modules():
        a = importlib.import_module(f'module_{module}')
        ret.append(a.get_obj()) 
    return ret
    
