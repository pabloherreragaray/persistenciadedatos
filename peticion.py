import json


class Peticion:
    operacion = None
    datos = None

    def __init__(self,operacion=None,datos=None):
        self.operacion = operacion
        self.datos = datos
    
    def a_json(self):
        return json.dumps({'operacion':self.operacion,'datos':self.datos})

    def desde_json(self,j):
        obj = json.loads(j)
        if isinstance(obj,dict):
            self.datos = obj.get('datos')
            self.operacion = obj.get('operacion')