import tkinter as tk
import tkinter.messagebox as tkmsg
import client_controller as cc


class FormularioBase(tk.Frame):
    def __init__(self,ventana_principal,padre=None):
        if padre is None: padre = ventana_principal
        tk.Frame.__init__(self,padre)
        self.ventana_principal = ventana_principal
        self.crear_gui()
    
    def crear_gui(self):
        pass


class FormularioLogin(FormularioBase):
    def crear_gui(self):
        label_cuenta = tk.Label(self,text=AplicacionGUI.apariencia['login']['label_cuenta'],
            width=25,anchor='e')
        label_cuenta.grid(row=0,column=0,padx=2,pady=2)
        self.texto_cuenta = tk.Entry(self)
        self.texto_cuenta.grid(row=0,column=1)
        label_clave = tk.Label(self,text=AplicacionGUI.apariencia['login']['label_clave'],
            width=25,anchor='e')
        label_clave.grid(row=1,column=0)
        self.texto_clave = tk.Entry(self, show='*')
        self.texto_clave.grid(row=1,column=1,padx=2,pady=2)
        boton_enviar = tk.Button(self,
            text=AplicacionGUI.apariencia['login']['boton_enviar'],
            command=self.click)
        boton_enviar.grid(row=2,column=0,columnspan=2,pady=10)
    
    def click(self):
        self.ventana_principal.enviar_login(self.texto_cuenta.get(),self.texto_clave.get())
    
    def reiniciar(self):
        self.texto_cuenta.delete(0,tk.END)
        self.texto_clave.delete(0,tk.END)


class FormularioMenuPrincipal(FormularioBase):
    def crear_gui(self):
        self.columnconfigure(0, weight=1)
        boton_consulta = tk.Button(self,text=AplicacionGUI.apariencia['menu']['boton_consulta'],
            command=self.click_consulta,width=25)
        boton_retiro = tk.Button(self,text=AplicacionGUI.apariencia['menu']['boton_retiro'],
            command=self.click_retiro,width=25)
        boton_abono = tk.Button(self,text=AplicacionGUI.apariencia['menu']['boton_abono'],
            command=self.click_abono,width=25)
        boton_regresar = tk.Button(self,text=AplicacionGUI.apariencia['menu']['boton_regresar'],
            command=self.click_regresar,width=25)
        botones = (boton_consulta, boton_retiro, boton_abono, boton_regresar)
        for i,b in enumerate(botones):
            b.grid(row=i,column=0,padx=10,pady=5)
    
    def click_consulta(self):
        self.ventana_principal.consultar()

    def click_retiro(self):
        self.ventana_principal.mostrar_retirar()

    def click_abono(self):
        self.ventana_principal.mostrar_abonar()

    def click_regresar(self):
        self.ventana_principal.mostrar_login()


class FormularioRetirarAbonar(FormularioBase):
    def crear_gui(self):
        self.accion = None
        self.columnconfigure(0,weight=1)
        self.label_retirar = tk.Label(self,text=AplicacionGUI.apariencia['retirar_abonar']['label_retirar'],
            font=AplicacionGUI.apariencia['retirar_abonar']['fuente_label'])
        self.label_retirar.grid(row=0,column=0,padx=10,pady=5)
        self.label_abonar = tk.Label(self,text=AplicacionGUI.apariencia['retirar_abonar']['label_abonar'],
            font=AplicacionGUI.apariencia['retirar_abonar']['fuente_label'])
        self.label_abonar.grid(row=0,column=0,padx=10,pady=5)
        self.texto_valor = tk.Entry(self)
        self.texto_valor.grid(row=1,column=0,padx=10,pady=5)
        boton_enviar = tk.Button(self,text=AplicacionGUI.apariencia['retirar_abonar']['boton_enviar'],
            width=25,command=self.click,font=AplicacionGUI.apariencia['retirar_abonar']['fuente_label'])
        boton_enviar.grid(row=2,column=0,padx=10,pady=5)
        boton_cancelar = tk.Button(self,text=AplicacionGUI.apariencia['retirar_abonar']['boton_cancelar'],
            width=20,command=self.click_cancelar)
        boton_cancelar.grid(row=3,column=0,padx=10,pady=5)
    
    def mostrar_retirar(self):
        self.accion = 'retirar'
        self.texto_valor.delete(0,tk.END)
        self.label_retirar.tkraise()

    def mostrar_abonar(self):
        self.accion = 'abonar'
        self.texto_valor.delete(0,tk.END)
        self.label_abonar.tkraise()
    
    def click(self):
        valor = self.texto_valor.get()
        if valor is None or len(valor)==0:
            tkmsg.showerror('Error','Debe ingresar el valor a %s'%self.accion)
            return
        try:
            nvalor = int(valor)
        except:
            tkmsg.showerror('Error','El valor debe ser un número válido')
            return
        self.ventana_principal.retirar_abonar(self.accion,nvalor)
    
    def click_cancelar(self):
        self.ventana_principal.mostrar_menu()


class AplicacionGUI(tk.Tk):
    apariencia = {
        'ancho_ventana':400,
        'alto_ventana':300,
        'fuente_titulo':'Helvetica 12 bold',
        'titulo':'Banco XYZ',
        'login':{
            'label_cuenta':'Ingrese su número de cuenta',
            'label_clave':'Ingrese su clave',
            'boton_enviar':'Enviar'
        },
        'menu':{
            'boton_consulta':'Consultar',
            'boton_retiro':'Retirar',
            'boton_abono':'Abonar',
            'boton_regresar':'Ingresar otra cuenta'
        },
        'retirar_abonar':{
            'label_retirar':'Ingrese la cantidad a retirar',
            'label_abonar':'Ingrese la cantidad a abonar',
            'fuente_label':'Helvetica 10 bold',
            'boton_enviar':'Enviar',
            'boton_cancelar':'Cancelar'
        }
    }

    def __init__(self):
        tk.Tk.__init__(self)
        self.controlador = cc.ControladorCliente()
        self.nombre_usuario = None
        self.numero_cuenta = None
        self.crear_gui()
    
    def crear_gui(self):
        self.title('Banco XYZ')
        self.geometry('%ix%i'%(self.apariencia['ancho_ventana'],self.apariencia['alto_ventana']))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.label_titulo = tk.Label(self,text=self.apariencia['titulo'],
            font=self.apariencia['fuente_titulo'],anchor=tk.CENTER)
        self.label_titulo.grid(row=0,column=0,sticky='WEN',pady=15)
        self.login = FormularioLogin(self)
        self.menu = FormularioMenuPrincipal(self)
        self.frmRetirarAbonar = FormularioRetirarAbonar(self)
        forms = (self.login,self.menu,self.frmRetirarAbonar)
        for f in forms:
            f.grid(row=1,column=0,sticky='WENS',pady=10, padx=10)
    
    def iniciar(self):
        self.mostrar_login()
        self.mainloop()
    
    def enviar_login(self,cuenta,clave):
        if cuenta is None or len(cuenta)==0:
            tkmsg.showerror('Error','Debe escribir su número de cuenta')
            return
        try:
            ncuenta = int(cuenta)
        except:
            tkmsg.showerror('Error','La cuenta debe ser un número')
            return
        if clave is None or len(clave)==0:
            tkmsg.showerror('Error','Debe escribir su clave')
            return
        try:
            resp = self.controlador.consulta_cliente(ncuenta,clave)
        except Exception as e:
            tkmsg.showerror('Error','Ocurrió un error al conectarse con el servidor. Inténtelo más tarde.')
            print(e)
            return
        if not resp.ok():
            tkmsg.showerror('Error',resp.error)
            return
        self.login_ok(ncuenta,resp.datos['nombre'])
    
    def login_ok(self,numero_cuenta,nombre_usuario):
        self.numero_cuenta = numero_cuenta
        self.nombre_usuario = nombre_usuario
        self.label_titulo.configure(text='Bienvenido(a) %s'%(self.nombre_usuario))
        self.mostrar_menu()
    
    def mostrar_login(self):
        self.label_titulo.configure(text=self.apariencia['titulo'])
        self.login.reiniciar()
        self.login.tkraise()

    def mostrar_menu(self):
        self.menu.tkraise()

    def mostrar_retirar(self):
        self.frmRetirarAbonar.mostrar_retirar()
        self.frmRetirarAbonar.tkraise()
    
    def mostrar_abonar(self):
        self.frmRetirarAbonar.mostrar_abonar()
        self.frmRetirarAbonar.tkraise()
    
    def consultar(self):
        try:
            resp = self.controlador.consulta(self.numero_cuenta)
        except Exception as e:
            tkmsg.showerror('Error','Error al consultar el servidor, inténtelo más tarde')
            print(e)
            return
        if not resp.ok():
            tkmsg.showerror('Error',resp.error)
            return
        tkmsg.showinfo('Proceso exitoso','Su saldo es de $%s'%str(resp.datos))

    def retirar_abonar(self,accion,valor):
        try:
            if accion=='abonar':
                resp = self.controlador.abono(self.numero_cuenta,valor)
            else:
                resp = self.controlador.retiro(self.numero_cuenta,valor)
        except Exception as e:
            tkmsg.showerror('Error','Error al consultar el servidor, inténtelo más tarde')
            print(e)
            return
        if not resp.ok():
            tkmsg.showerror('Error',resp.error)
            return
        tkmsg.showinfo('Proceso exitoso','El %s se hizo correctamente'%('abono' if accion=='abonar' else 'retiro'))
        self.mostrar_menu()

