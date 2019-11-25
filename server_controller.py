import peticion
import respuesta
import logs


log = logs.get_logger('Servidor-Ctrl')


class ControladorServidor:
    def procesar_peticion(self,pet,resp):
        if not isinstance(pet,peticion.Peticion):
            raise Exception('Se esperaba una peticion')
        if not isinstance(resp,respuesta.Respuesta):
            raise Exception('Se esperaba una respuesta')
        if pet.operacion=='retiro':
            resp.set_datos(self.retiro(pet.datos))

    def retiro(self,dato):
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        resp = 'Retiro exitoso' #TODO
        #log.info('Retiro cuenta %s, valor %s = %s'%(cuenta,valor,resp))
        return resp
    
    def abono(self,dato):
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        resp = 'Abono exitoso' #TODO
        #log.info('Abono cuenta %s, valor %s = %s'%(cuenta,valor,resp))
        return resp

    def consulta(self,dato):
        cuenta = dato.get('cuenta')
        resp = 200000 #TODO
        #log.info('Consulta cuenta %s = %s'%(cuenta,resp))
        return resp
