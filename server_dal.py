import psycopg2
import decimal
import datetime


SQLS = {
    'consulta_cliente':'''
select concat(nombres,' ',apellidos) as nombre,
	case when password={{contrasena}} then 1
	else 0 end as clavecorrecta
from cuentas as cu
inner join clientes as cli on cu.idcliente=cli.idcliente
where nocuenta={{cuenta}}
    ''',
    'retiro':'''
UPDATE cuentas SET saldo = saldo - {{valor}} WHERE nocuenta={{cuenta}}
    ''',
    'abono':'''
UPDATE cuentas SET saldo = saldo + {{valor}} WHERE nocuenta={{cuenta}}
    ''',
    'get_saldo_cuenta':'''
SELECT saldo FROM cuentas WHERE nocuenta={{cuenta}}
    ''',
    'transaccion':'''
INSERT INTO transacciones (tipotransaccion,idcuenta,valortransaccion,fechatransaccion,iporigen)
VALUES ({{tipotransaccion}},{{idcuenta}},{{valortransaccion}},{{fechatransaccion}},{{iporigen}})
    ''',
    'get_id_cuenta':'''
SELECT idcuenta FROM cuentas WHERE nocuenta={{cuenta}}
    '''
}

TIPO_TRANSACCION_ABONO = 1
TIPO_TRANSACCION_RETIRO = 2


class DataAccessLayer:
    def ejecutar_query(self,sql):
        con = self.get_conexion()
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        con.close()
        return res
    
    def ejecutar_query_one(self,sql):
        res = self.ejecutar_query(sql)
        return None if res is None or len(res)==0 else res[0]
    
    def ejecutar_query_escalar(self,sql):
        res = self.ejecutar_query_one(sql)
        return None if res is None else res[0]
    
    def ejecutar_no_query(self,sql):
        con = self.get_conexion()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def get_sql(self,nombresql,variables):
        sql = SQLS.get(nombresql)
        if sql is None or sql=='': return None
        if variables is not None and isinstance(variables,dict):
            for k,v in variables.items():
                if v is None: vv = 'NULL'
                elif isinstance(v,str): vv = "'%s'"%str(v)
                else: vv = str(v)
                sql = sql.replace('{{%s}}'%k,vv)
        return sql

    def consulta_cliente(self,cuenta,contrasena):
        sql = self.get_sql('consulta_cliente',{'cuenta':cuenta,'contrasena':str(contrasena) if contrasena is not None else ''})
        try:
            cuenta = self.ejecutar_query_one(sql)
        except Exception as e:
            return '','Error al consultar la base de datos: %s'%str(e)
        if cuenta is None: return '','Cuenta no existe'
        else:
            nombre,clavecorrecta = cuenta
            if clavecorrecta==1:
                return nombre,''
            else:
                return '','Clave incorrecta'

    def consulta(self,cuenta):
        try:
            saldo = self.get_saldo_cuenta(cuenta)
        except Exception as e:
            return '','Error al consultar la base de datos: %s'%str(e)
        if saldo is None or not isinstance(saldo,(int,float,decimal.Decimal)):
            return '','Cuenta no existe'
        else:
            return float(saldo),''
    
    def get_saldo_cuenta(self,cuenta):
        return self.ejecutar_query_escalar(self.get_sql('get_saldo_cuenta',{'cuenta':cuenta}))
    
    def get_id_cuenta(self,cuenta):
        return self.ejecutar_query_escalar(self.get_sql('get_id_cuenta',{'cuenta':cuenta}))

    def retiro(self,cuenta,valor,ip):
        sql = self.get_sql('retiro',{'cuenta':cuenta,'valor':valor})
        saldo = self.get_saldo_cuenta(cuenta)
        if saldo is None or not isinstance(saldo,(int,float,decimal.Decimal)):
            return '','Cuenta no existe'
        elif valor>saldo:
            return '','Fondos insuficientes'
        try:
            self.ejecutar_no_query(sql)
            self.crear_transaccion(TIPO_TRANSACCION_RETIRO,cuenta,valor,ip)
            return True,''
        except Exception as e:
            return '','Error al consultar la base de datos: %s'%str(e)

    def abono(self,cuenta,valor,ip):
        sql = self.get_sql('abono',{'cuenta':cuenta,'valor':valor})
        saldo = self.get_saldo_cuenta(cuenta)
        if saldo is None or not isinstance(saldo,(int,float,decimal.Decimal)):
            return '','Cuenta no existe'
        try:
            self.ejecutar_no_query(sql)
            self.crear_transaccion(TIPO_TRANSACCION_ABONO,cuenta,valor,ip)
            return True,''
        except Exception as e:
            return '','Error al consultar la base de datos: %s'%str(e)
    
    def crear_transaccion(self,tipo,cuenta,valor,ip):
        try:
            sql = self.get_sql('transaccion',{
                'tipotransaccion':tipo,
                'idcuenta':self.get_id_cuenta(cuenta),
                'valortransaccion':valor,
                'fechatransaccion':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S -05:00'),
                'iporigen':ip
            })
            print(sql)
            self.ejecutar_no_query(sql)
        except: pass

    def get_conexion(self):
        return psycopg2.connect(database="dfb5vac11fb6k4", user="oqqoveqsnrntmv", password="c3724eebd6e00b3dffe62b8b8eb1da1fe0b1bf87f218fe98697bbf7e3f1437af", host="ec2-54-225-72-238.compute-1.amazonaws.com", port="5432")

if __name__=='__main__':
    dal = DataAccessLayer()
    con = dal.get_conexion()
    cur = con.cursor()
    res = cur.callproc('public.retirar',[410600800,123199,])
    print(res)
    con.close()
