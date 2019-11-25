import peticion
import respuesta
import logs


log = logs.get_logger('Servidor-Ctrl')


# Datos de ejemplo
datos_ejemplo = {
    12345: {
        'saldo': 100000,
        'nombre': 'Pablo Herrera Garay',
        'contrasena':'12345'
    },
    123: {
        'saldo': 0,
        'nombre': 'Fulano',
        'contrasena':'12345'
    },
    321: {
        'saldo': 5000000,
        'nombre': 'Mengano',
        'contrasena':'12345'
    }
}


class ControladorServidor:
    def procesar_peticion(self,pet,resp):
        if not isinstance(pet,peticion.Peticion):
            raise Exception('Se esperaba una peticion')
        if not isinstance(resp,respuesta.Respuesta):
            raise Exception('Se esperaba una respuesta')
        if pet.operacion=='retiro':
            #Si la operación es retiro
            resp.set_datos(self.retiro(pet.datos))
        elif pet.operacion=='consulta_cliente':
            #Si la operación es consulta de cliente
            resp.set_datos(self.consulta_cliente(pet.datos))
        elif pet.operacion=='consulta':
            #Si la operación es consulta de saldo
            resp.set_datos(self.consulta(pet.datos))
        elif pet.operacion=='abono':
            #Si la operación es abono
            resp.set_datos(self.abono(pet.datos))

    def consulta_cliente(self,dato):
        '''Consulta el cliente por su numero de cuenta
        '''
        cuenta = dato.get('cuenta')
        contrasena = dato.get('contrasena')
        #TODO En la siguiente linea se hace la conexion con la base de datos
        datos = datos_ejemplo.get(cuenta)
        if datos is None:
            raise Exception('Cuenta no existe')
        else:
            if datos.get('contrasena')!=contrasena:
                raise Exception('Clave erronea')
            else:
                return {'ok':True,'error':'','nombre':datos.get('nombre')}

    def retiro(self,dato):
        '''Retira del saldo de la cuenta, siempre y
        cuando la cuenta exista y tenga saldo suficiente
        '''
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        if not isinstance(valor,int):
            raise Exception('El valor no es valido')
        if valor<=0:
            raise Exception('El valor debe ser superior a cero')
        #TODO En la siguiente linea se hace la conexion con la base de datos
        datos = datos_ejemplo.get(cuenta)
        if datos is None:
            raise Exception('Cuenta no existe')
        saldo = datos.get('saldo')
        if valor>saldo:
            raise Exception('Fondos insuficientes')
        datos['saldo'] = saldo-valor
        return 'Retiro exitoso'
    
    def abono(self,dato):
        '''Realiza un abono siempre y cuando la cuenta exista
        '''
        cuenta = dato.get('cuenta')
        valor = dato.get('valor')
        if not isinstance(valor,int):
            raise Exception('El valor no es valido')
        #TODO En la siguiente linea se hace la conexion con la base de datos
        datos = datos_ejemplo.get(cuenta)
        if datos is None:
            raise Exception('Cuenta no existe')
        saldo = datos.get('saldo')
        datos['saldo'] = saldo+valor
        return 'Abono exitoso'

    def consulta(self,dato):
        '''Realiza la consulta del saldo siempre y cuando
        la cuenta exista
        '''
        cuenta = dato.get('cuenta')
        #TODO En la siguiente linea se hace la conexion con la base de datos
        datos = datos_ejemplo.get(cuenta)
        if datos is None:
            raise Exception('Cuenta no existe')
        return datos.get('saldo')
