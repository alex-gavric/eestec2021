from Module import Module
from jsonRW import read_json_file

import time
import abuseipdb


class AbudeIpDb(Module):
    
    def __init__(self):
        # cita svoj API_KEY iz json-a    # ako ne nadje je None
        self.API_KEY = read_json_file("api_keys.json").get(self.__class__.__name__)
        
        abuseipdb.configure_api_key(self.API_KEY)
        #self.client = vt.Client(self.API_KEY)

    
    def send_hash(self, hash_str):
        return self.send_url(hash_str)

    def send_file(self, location_of_file):
        return {"type":"error","message":"not implemented", 'name' : self.__class__.__name__ }
                
    def send_url(self, string):
        response = abuseipdb.check_ip(ip=string,days="30")
        print(response)
        return {"type":"error","message":'response', 'name' : self.__class__.__name__ }
    
    def send_ip(self, string):
        return self.send_url(string)
    
    def get_data(self,data):        
        ret = {'type':'report', 'name' : self.__class__.__name__ }
        ret['malicious'] = data.get('suspicious', 0) + data.get('malicious', 0)
        ret['undetected'] = data.get('harmless', 0) + data.get('undetected', 0)
        ret["message"] = "Malicious: " + ret['malicious'] + ", Undetected: " + ret['undetected']
        return ret

    
def get_obj(): return AbudeIpDb()
