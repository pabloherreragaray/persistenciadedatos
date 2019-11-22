import socketserver
import logs
import server_controller
import peticion
import respuesta


TAMANO_BUFFER = 10240
HOST = '127.0.0.1'
PUERTO = 8888

log = logs.get_logger('Servidor')

controlador = server_controller.ControladorServidor()

class ServidorHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = str(self.request.recv(TAMANO_BUFFER),'utf-8').strip()
            log.info('%s envio: %s'%(self.client_address,data))
            pet = peticion.Peticion()
            resp = respuesta.Respuesta()
            try:
                pet.desde_json(data)
            except:
                error = 'Los datos suministrados no tienen formato JSON: %s'%data
                resp.set_error(error)
                log.error(error)
            if not resp.en_error():
                try:
                    controlador.procesar_peticion(pet,resp)
                except Exception as e:
                    error = 'Error al procesar la peticion: %s'%str(e)
                    resp.set_error(error)
                    log.error(error)
            self.request.sendall(bytes(resp.a_json(),'utf-8'))
        except Exception as e:
            log.error(str(e))


class Servidor:
    def iniciar(self):
        socksrv = socketserver.TCPServer((HOST,PUERTO),ServidorHandler)
        log.info('Servidor inicia ejecucion')
        socksrv.serve_forever()

if __name__=='__main__':
    srv = Servidor()
    srv.iniciar()