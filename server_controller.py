import peticion
import respuesta
import logs
import server_dal


log = logs.get_logger('Servidor-Ctrl')


class ControladorServidor:
    def __init__(self):
        self.dal = server_dal.DataAccessLayer()

    def procesar_peticion(self,pet,resp):
        if not isinstance(pet,peticion.Peticion):
            raise Exception('Se esperaba una peticion')
        if not isinstance(resp,respuesta.Respuesta):
            raise Exception('Se esperaba una respuesta')
        if pet.operacion=='retiro':
            #Si la operación es retiro
            resp.set_datos(self.retiro(pet.datos,resp.iporigen[0]))
        elif pet.operacion=='consulta_cliente':
            #Si la operación es consulta de cliente
            resp.set_datos(self.consulta_cliente(pet.datos))
        elif pet.operacion=='consulta':
            #Si la operación es consulta de saldo
            resp.set_datos(self.consulta(pet.datos))
        elif pet.operacion=='abono':
            #Si la operación es abono
            resp.set_datos(self.abono(pet.datos,resp.iporigen[0]))

    def consulta_cliente(self,dato):
        '''Consulta el cliente por su numero de cuenta
        '''
        cuenta = dato.get('cuenta')
        contrasena = dato.get('contrasena')
        nombre,error = self.dal.consulta_cliente(cuenta,contrasena)
        if error is not None and len(error)>0:
            raise Exception(error)
        else:
            return {'ok':True,'error':'','nombre':nombre}

    def retiro(self,dato,ip):
        '''Retira del saldo de la cuenta, siempre y
        cuando la cuenta exista y tenga saldo suficiente
        '''
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        if not isinstance(valor,int):
            raise Exception('El valor no es valido')
        if valor<=0:
            raise Exception('El valor debe ser superior a cero')
        _,error = self.dal.retiro(cuenta,valor,ip)
        if error is not None and len(error)>0:
            raise Exception(error)
        else: return 'Retiro exitoso'
    
    def abono(self,dato,ip):
        '''Realiza un abono siempre y cuando la cuenta exista
        '''
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        if not isinstance(valor,int):
            raise Exception('El valor no es valido')
        _,error = self.dal.abono(cuenta,valor,ip)
        if error is not None and len(error)>0:
            raise Exception(error)
        else: return 'Abono exitoso'

    def consulta(self,dato):
        '''Realiza la consulta del saldo siempre y cuando
        la cuenta exista
        '''
        cuenta = dato.get('cuenta')
        saldo,error = self.dal.consulta(cuenta)
        if error is not None and len(error)>0:
            raise Exception(error)
        else: return saldo
