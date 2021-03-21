import os
import json

def read_json_file(file_location,default_value=None):
    if not os.path.isfile(file_location):
        write_json_file(file_location,default_value)
        return default_value
    with open(file_location, 'r') as f:
        data=f.read()
    return json.loads(data) 
    
def write_json_file(file_location,json_data):        
    with open(file_location, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

