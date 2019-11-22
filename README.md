# Entrega Persistencia de Datos
## Sockets con Python

Repositorio de código para las entregas del módulo de persistencia de datos, Politécnico Grancolombiano, 2019.

## Requisitos
- Python 3

## Instrucciones de ejecución
1. En Windows ejecutar el archivo "servidor.bat". En Linux ejecutar "python server.py". Esto pondrá en funcionamiento el servidor.
2. En Windows ejecutar el archivo "cliente.bat". En Linux ejecutar "python client_controller.py". Esto ejecutará la prueba con el cliente.

## Funcionamiento

### Servidor
La clase server.Servidor hace uso de "socketserver" para abrir un hilo de ejecución con cada conexión entrante. Los datos recibidos (en formato JSON) son convertidos en objetos, los cuales se pasan al server_controller.ControladorServidor, quien determina como procesarlos.

La petición en formato JSON debe contener este formato:

```javascript
{
  "operacion": "", //Es una cadena con el nombre de la función que debe ejecutar el controlador.
  "datos": {} //Es un objeto con los datos que se desea procesar.
}
```

El resultado del procesamiento es entregado por el servidor en el siguiente formato JSON:

```javascript
{
  "datos": {}, //Es un objeto con la respuesta devuelta por el controlador.
  "error": "" //Es una cadena con el mensaje de error, de haberlo. En otro caso es null.
}
```

### Cliente
La clase client_controller.ControladorCliente es la parte controladora del cliente. Tiene una instancia de la clase client.Cliente, que se encarga de enviar las peticiones al servidor, recibir las respuestas y devolverlas al controlador.

### Transacción
1. El controlador del cliente le pasa la petición al cliente, indicando operación y datos.
2. El cliente convierte la petición en JSON y la pasa al servidor.
3. El servidor abre un hilo con la conexión del cliente y recibe el dato como JSON.
4. El servidor convierte el JSON de nuevo a petición y se lo pasa al controlador de servidor.
5. El controlador de servidor procesa la petición y devuelve una respuesta al servidor.
6. El servidor convierte la respuesta en JSON y la envía al cliente.
7. El cliente convierte el JSON recibido nuevamente en una respuesta y se la pasa al controlador del cliente.
8. El cliente cierra la conexión.
9. El servidor recibe el cierre y "mata" al hilo.

## Pasos a seguir
Con este modelo de transacción solo hace falta desarrollar las funcionalidades del aplicativo en los dos controladores (cliente y servidor). Ambos manejan sus datos como objetos o diccionarios de Python (envueltos por las clases peticion.Peticion y respuesta.Respuesta) y se "despreocupan" por la transaccionalidad y conversión a JSON.
