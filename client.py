import socket
import logs
import peticion
import respuesta


TAMANO_BUFFER = 10240
HOST = '127.0.0.1'
PUERTO = 8888

log = logs.get_logger('Cliente')


class Cliente:
    def enviar_peticion(self,datos):
        if not isinstance(datos,peticion.Peticion):
            raise Exception('Se esperaba una peticion')
        datos = datos.a_json()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PUERTO))
        log.info('Conectado al servidor')
        sock.sendall(bytes(datos+'\n','utf-8'))
        recv = str(sock.recv(TAMANO_BUFFER),'utf-8')
        log.info('Respuesta desde el servidor: %s'%recv)
        sock.close()
        datos = respuesta.Respuesta()
        datos.desde_json(recv)
        return datos
