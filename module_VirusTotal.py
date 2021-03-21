from Module import Module
from jsonRW import read_json_file

import time
import vt


class VirusTotal(Module):
    
    def __init__(self):
        # cita svoj API_KEY iz json-a    # ako ne nadje je None
        self.API_KEY = read_json_file("api_keys.json").get(self.__class__.__name__)
    
        self.client = vt.Client(self.API_KEY)

    
    def send_hash(self, hash_str):
        try:
            file = self.client.get_object(f"/files/{hash_str}")
            return self.get_data(file.last_analysis_stats)
        except Exception as e:
            if 'NotFoundError' in str(e):
                return {"type":"error","message":"hash not found", 'name' : self.__class__.__name__ }

    def send_file(self, location_of_file):
        try:
            hash_str = self.hash_of_file(location_of_file)
            if not hash_str: raise Exception('NotFoundError')
            file = self.client.get_object(f"/files/{hash_str}")
            return self.get_data(file.last_analysis_stats)
        except Exception as e:
            try:
                if 'NotFoundError' in str(e):
                    with open(location_of_file, "rb") as f:
                        analysis = self.client.scan_file(hash_str)
                    return self._wait(analysis)
            except Exception as e:
                return {"type":"error","message":"not valid file path", 'name' : self.__class__.__name__ }
                
    def send_url(self, string):
        try:
            url_id = vt.url_id(string)
            url = self.client.get_object(f"/urls/{url_id}")
            return self.get_data(url.last_analysis_stats)
        except Exception as e:
            try:
                if 'NotFoundError' in str(e):
                    analysis = self.client.scan_url(string)
                    return self._wait(analysis)
            except Exception as e:
                if 'InvalidArgumentError' in str(e):
                    return {"type":"error","message":'not valid url', 'name' : self.__class__.__name__ }
    
    def send_ip(self, string):
        return self.send_url(string)
    
    def _wait(self, analysis):
        for _ in range(10):
            analysis = self.client.get_object("/analyses/{}", analysis.id)
            print(analysis.status)
            if analysis.status == "completed":
                return self.get_data(analysis.stats)
            time.sleep(30)
        return {"type":"error","message":"timeout", 'name' : self.__class__.__name__ } #after 10*30 sec      

    def get_data(self,data):        
        ret = {'type':'report', 'name' : self.__class__.__name__ }
        ret['malicious'] = data.get('suspicious', 0) + data.get('malicious', 0)
        ret['undetected'] = data.get('harmless', 0) + data.get('undetected', 0)
        ret["message"] = "Malicious: " + ret['malicious'] + ", Undetected: " + ret['undetected']
        return ret


    def close(self):
        self.client.close()
    
def get_obj(): return VirusTotal()
