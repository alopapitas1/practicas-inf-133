from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs




class mensajesService:
    @staticmethod
    def find_mensaje(id):
        return next(
            (mensaje for mensaje in mensajes if mensaje["id"] == id),
            None,
        )

    @staticmethod
    def encript_msj(mensaje):
        pal=mensaje
        asci_list=[]
        for caract in pal:
            v_ascii=ord(caract)
            asci_list.append(v_ascii+3)
        
        pala_con=''.join(chr(valor) for valor in asci_list)
        return pala_con
        

    @staticmethod
    def add_mensaje(data):
        data["id"] = len(mensajes) + 1
        
        
        mensaje = data["mensaje"]
        encriptado = mensajesService.encript_msj(mensaje)
        data["encriptado"] = encriptado
        mensajes.append(data)
        return data

    @staticmethod
    def update_mensaje(id, data):
        mensaje = mensajesService.find_mensaje(id)
        if mensaje:
        # Actualiza los campos relevantes del mensaje
            for key, value in data.items():
                if key != "id":
                    mensaje[key] = value
        
            if "mensaje" in data:
                mensaje["encriptado"] = mensajesService.encript_msj(data["mensaje"])
            
            return mensaje
        else:
            return None

    @staticmethod
    def delete_mensaje():
        mensajes.clear()
        return mensajes
    
    @staticmethod
    def delete_mensaje_id(id):
        for mensaje in mensajes:
            if mensaje["id"] == id:
                mensajes.remove(mensaje)
                return mensaje
        return None
    
    
    @staticmethod
    def get_instance():
        if encriptado is None:
            encriptado = encriptado()
        return encriptado



mensajes = [
    {
        "id": 1,
        "mensaje": "ab",
        "encriptado":mensajesService.encript_msj("ab")
    },
]


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 200, mensajes)
        
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = mensajesService.find_mensaje(id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, [mensaje])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            mensajes = mensajesService.add_mensaje(data)
            HTTPResponseHandler.handle_response(self, 201, mensajes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            mensajes = mensajesService.update_mensaje(id, data)
            if mensajes:
                HTTPResponseHandler.handle_response(self, 200, mensajes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "mensaje no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/mensajes":
            mensajes = mensajesService.delete_mensaje()
            HTTPResponseHandler.handle_response(self, 200, mensajes)
            
            
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = mensajesService.delete_mensaje_id(id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, [mensaje])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])    
            
            
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )



    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
