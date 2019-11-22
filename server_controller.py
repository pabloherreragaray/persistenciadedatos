import peticion
import respuesta
import logs


log = logs.get_logger('Controlador Servidor')


class ControladorServidor:
    def procesar_peticion(self,pet,resp):
        if not isinstance(pet,peticion.Peticion):
            raise Exception('Se esperaba una peticion')
        if not isinstance(resp,respuesta.Respuesta):
            raise Exception('Se esperaba una respuesta')
        if pet.operacion=='prueba_conexion':
            resp.set_datos(self.prueba_conexion(pet.datos))

    def prueba_conexion(self,dato):
        s = str(dato) if dato is not None else ''
        s = s.upper()
        return s
