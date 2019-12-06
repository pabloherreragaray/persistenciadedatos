import json


class Respuesta:
    datos = None
    error = None
    iporigen = None

    def set_datos(self,datos):
        self.datos = datos
    
    def set_error(self,error):
        if error is None: return
        self.error = str(error)
    
    def en_error(self):
        return self.error is not None and len(self.error)>0
    
    def ok(self):
        return not self.en_error()
    
    def a_json(self):
        return json.dumps({'datos':self.datos,'error':self.error})
    
    def desde_json(self,j):
        obj = json.loads(j)
        if isinstance(obj,dict):
            self.datos = obj.get('datos')
            self.error = obj.get('error')
