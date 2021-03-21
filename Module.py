import hashlib

class Module:
    def __init__(self, *arg, **kwarg):
        pass
        
    
    def send_file(self, *arg, **kwarg):
        return None
    def send_hash(self, *arg, **kwarg):
        return None
    def send_domen(self, *arg, **kwarg):
        return None
    def send_ip(self, *arg, **kwarg):
        return None
    def send_url(self, *arg, **kwarg):
        return None
        
    def hash_of_file(self, file):
        try:
            BLOCK_SIZE = 65536
            file_hash = hashlib.sha256()
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    file_hash.update(fb)
                    fb = f.read(BLOCK_SIZE) 

            return file_hash.hexdigest()
        except:
            return None
