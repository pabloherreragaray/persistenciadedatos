import sys

class AplicacionConsola:
    ESTADO_SALIR_DEL_PROGRAMA = 'salir'
    ESTADO_INICIO = 'inicio'
    ESTADO_MENU_PRINCIPAL = 'menu_principal'
    ESTADO_CONSULTA = 'consulta'

    numero_cuenta = 0

    def __init__(self):
        self.cambiar_estado(self.ESTADO_INICIO)

    def cambiar_estado(self,estado):
        self.estado_actual = estado
        if self.estado_actual==self.ESTADO_MENU_PRINCIPAL:
            self.menu_principal()
        elif estado==self.ESTADO_CONSULTA:
            self.consultar()
        elif estado==self.ESTADO_INICIO:
            self.inicio()
    
    def consultar(self):
        self.mostrar_encabezado_principal('Consultar')

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
            #TODO
            ok = True
            if ok:
                self.numero_cuenta = nro_cuenta
                self.cambiar_estado(self.ESTADO_MENU_PRINCIPAL)
                break
            else:
                self.mostrar_error('La cuenta no existe')
                continue

    def menu_principal(self):
        self.mostrar_encabezado_principal('Menu Principal Cuenta %i'%self.numero_cuenta)
        estados = [
            ['Consultar', self.ESTADO_CONSULTA],
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
        print(' NOMBRE '.center(80,'='))
        print((' '+nombresubmenu+' ').center(80,'-'))

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


if __name__=='__main__':
    AplicacionConsola()