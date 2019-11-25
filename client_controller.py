import client
import peticion
import logs


log = logs.get_logger('Cliente-Ctrl')


class ControladorCliente:
    def __init__(self):
        self.cliente = client.Cliente()
    
    def retiro(self,cuenta,valor):
        pet = peticion.Peticion('retiro',{'cuenta':cuenta,'valor':valor})
        resp = self.cliente.enviar_peticion(pet)
        #log.info('Retiro cuenta: %s, valor: %s, respuesta: %s'%(cuenta,valor,resp.__dict__))
        return resp

    def abono(self,cuenta,valor):
        pet = peticion.Peticion('abono',{'cuenta':cuenta,'valor':valor})
        resp = self.cliente.enviar_peticion(pet)
        #log.info('Retiro cuenta: %s, valor: %s, respuesta: %s'%(cuenta,valor,resp.__dict__))
        return resp

    def consulta(self,cuenta):
        pet = peticion.Peticion('consulta',{'cuenta':cuenta})
        resp = self.cliente.enviar_peticion(pet)
        #log.info('Retiro cuenta: %s, respuesta: %s'%(cuenta,resp.__dict__))
        return resp


if __name__=='__main__':
    ctrl = ControladorCliente()
    resp = ctrl.retiro(1234568, 100000)
    print(resp.__dict__)
    resp = ctrl.abono(12345678, 200000)
    print(resp.__dict__)
    rep = ctrl.consulta(12345678)
    print(resp.__dict__)
