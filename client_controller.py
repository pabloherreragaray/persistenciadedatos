import client
import peticion


class ControladorCliente:
    def __init__(self):
        self.cliente = client.Cliente()
    
    def prueba_conexion(self):
        pet = peticion.Peticion('prueba_conexion','Hola Mundo')
        resp = self.cliente.enviar_peticion(pet)
        print(resp.__dict__)


if __name__=='__main__':
    ctrl = ControladorCliente()
    ctrl.prueba_conexion()
