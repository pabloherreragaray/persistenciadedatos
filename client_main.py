import sys
import client_controller
from client_main_gui import AplicacionGUI

class AplicacionConsola:
    ESTADO_SALIR_DEL_PROGRAMA = 'salir'
    ESTADO_INICIO = 'inicio'
    ESTADO_MENU_PRINCIPAL = 'menu_principal'
    ESTADO_CONSULTA = 'consulta'
    ESTADO_RETIRO = 'retiro'
    ESTADO_ABONO = 'abono'

    numero_cuenta = 0
    nombre_cliente = ''

    def __init__(self):
        self.controlador = client_controller.ControladorCliente()
        self.cambiar_estado(self.ESTADO_INICIO)

    def cambiar_estado(self,estado):
        self.estado_actual = estado
        if self.estado_actual==self.ESTADO_MENU_PRINCIPAL:
            self.menu_principal()
        elif estado==self.ESTADO_CONSULTA:
            self.consultar()
        elif estado==self.ESTADO_INICIO:
            self.inicio()
        elif estado==self.ESTADO_ABONO:
            self.abono()
        elif estado==self.ESTADO_RETIRO:
            self.retiro()
    
    def consultar(self):
        self.mostrar_encabezado_principal('Consultar')
        try:
            resp = self.controlador.consulta(self.numero_cuenta)
            print('Su saldo es: $%s'%resp.datos)
        except:
            self.mostrar_error_conexion()
        print('')
        print('(1) para regresar al menu, (2) para salir')
        val = input()
        if val=='2':
            self.salir_del_programa()
        else:
            self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)
    
    def retiro(self):
        self.mostrar_encabezado_principal('Retiro')
        valor_monto = 0
        while True:
            print('Ingrese monto a retirar (0 para regresar)')
            monto = input()
            if monto=='0':
                self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)
                return
            try:
                valor_monto = int(monto)
                if valor_monto<0:
                    raise Exception('')
                break
            except:
                self.mostrar_error('Debe ingresar un numero mayor que cero')
        if valor_monto>0:
            resp = self.controlador.retiro(self.numero_cuenta,valor_monto)
            if resp.ok():
                print(resp.datos)
            else:
                self.mostrar_error(resp.error)
        print('')
        print('(1) para regresar al menu, (2) para salir')
        val = input()
        if val=='2':
            self.salir_del_programa()
        else:
            self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)

    def abono(self):
        self.mostrar_encabezado_principal('Abono')
        valor_monto = 0
        while True:
            print('Ingrese monto a abonar (0 para regresar)')
            monto = input()
            if monto=='0':
                self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)
                return
            try:
                valor_monto = int(monto)
                if valor_monto<0:
                    raise Exception('')
                break
            except:
                self.mostrar_error('Debe ingresar un numero mayor que cero')
        if valor_monto>0:
            resp = self.controlador.abono(self.numero_cuenta,valor_monto)
            if resp.ok():
                print(resp.datos)
            else:
                self.mostrar_error(resp.error)
        print('')
        print('(1) para regresar al menu, (2) para salir')
        val = input()
        if val=='2':
            self.salir_del_programa()
        else:
            self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)

    def inicio(self):
        self.mostrar_encabezado_principal('Inicio')
        while True:
            print('Ingrese su numero de cuenta (0 para salir)')
            cuenta = input()
            nro_cuenta = 0
            try:
                nro_cuenta = int(cuenta)
            except:
                self.mostrar_error('Debe escribir el numero de su cuenta')
                continue
            if nro_cuenta==0:
                self.salir_del_programa()
                return
            elif nro_cuenta<0:
                self.mostrar_error('El numero de cuenta debe ser mayor de 0')
                continue
            print('Ahora ingrese la clave')
            clave = input()
            try:
                resp = self.controlador.consulta_cliente(nro_cuenta,clave)
            except:
                self.mostrar_error_conexion()
                continue
            ok = resp.ok()
            if ok:
                self.numero_cuenta = nro_cuenta
                self.nombre_cliente = resp.datos.get('nombre')
                self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)
                break
            else:
                self.mostrar_error(resp.error)
                continue

    def menu_principal(self):
        self.mostrar_encabezado_principal('Bienvenido(a) %s'%self.nombre_cliente)
        estados = [
            ['Consultar', self.ESTADO_CONSULTA],
            ['Hacer retiro',self.ESTADO_RETIRO],
            ['Hacer abono',self.ESTADO_ABONO],
            ['Ingresar otra cuenta',self.ESTADO_INICIO]
        ]
        textos = [x[0] for x in estados]
        salir,numero = self.mostrar_menu(textos)
        if salir:
            self.salir_del_programa()
            return
        estado = estados[numero-1][1]
        self.cambiar_estado(estado)

    def mostrar_encabezado_principal(self, nombresubmenu):
        print('')
        print(' BANCO XYZ '.center(80,'='))
        print((' '+nombresubmenu+' ').center(80,'-'))
        print('')

    def salir_del_programa(self):
        print(' FIN DEL PROGRAMA '.center(80,'='))
        sys.exit()

    def mostrar_menu(self,opciones):
        print('Seleccione una opcion')
        for i,opcion in enumerate(opciones):
            print('(%i) %s'%(i+1,opcion))
        print('(%i) Salir'%(len(opciones)+1))
        s = input()
        try:
            numero = int(s)
            if numero<1 or numero>len(opciones)+1:
                raise ''
            salir = numero==len(opciones)+1
            return salir,numero
        except:
            self.mostrar_error('Debe escribir una de las opciones listadas')
            return self.mostrar_menu(opciones)
    
    def mostrar_error(self,mensaje):
        print('[ '+((' '+mensaje+' ').center(76,'*'))+' ]')
    
    def mostrar_error_conexion(self):
        self.mostrar_error('No se pudo establecer conexion con el servidor. Intentelo mas tarde')


def consola():
    AplicacionConsola()


def gui():
    app = AplicacionGUI()
    app.iniciar()


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[0]=='consola':
        consola()
    else:
        gui()
