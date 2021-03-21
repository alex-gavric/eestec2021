import re
import redis
from Agent import *

rds = redis.Redis(host='localhost', port=6379, db=0)
reg = r"[^a-zA-Z0-9.,;'\":\ !$%&*\(\)\+\-\\\?\/\~\`\{\}\[\]\<\>\€\?\_]+"

dirModules = list_of_modules()
modulesObjects = list_of_objects()
print(dirModules, modulesObjects)


def GetList():
    return {"modules": dirModules }

def Decode(bytesStr):
    if bytesStr is not None:
        return bytesStr.decode("utf-8")
    else:
        return None
    
def SearchIP(ip):
    outputs = []
    count = 0
    for module in modulesObjects:
        print(module.__class__.__name__)
        result = module.send_ip(ip)
        print(result)
        if result is None:
            result = {'name': module.__class__.__name__, 'message': 'Scanning performed. Unknown input.', 'detected' : 0}
        else:
            if result['message'] == "detected":
                    count+=1
            if 'detected' in result.keys():
                count += int(result['detected'])
        outputs.append(result)
    print(outputs)
    return { "modules": outputs, "risk" : count}