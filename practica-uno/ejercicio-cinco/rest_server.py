from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "lobo",
        "Especie": "cazador",
        "Género": "macho",
        "Edad":"22",
        "Peso": "11"
    },
]


class animalesService:
    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )

    @staticmethod
    def filter_animal_by_especi(Especie):
        return [
            animal for animal in animales if animal["Especie"] == Especie
        ]

    @staticmethod
    def filter_animal_by_genero(Género):
        return [
            animal for animal in animales if animal["Género"] == Género
        ]

    @staticmethod
    def add_student(data):
        data["id"] = len(animales) + 1
        animales.append(data)
        return animales

    @staticmethod
    def update_animal(id, data):
        animal = animalesService.find_animal(id)
        if animal:
            animal.update(data)
            return animal
        else:
            return None

    @staticmethod
    def delete_animal():
        animales.clear()
        return animales
    
    @staticmethod
    def delete_animal_id(id):
        for animal in animales:
            if animal["id"] == id:
                animales.remove(animal)
                return animal
        return None


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

        if parsed_path.path == "/animales":
            if "Especie" in query_params:
                Especie = query_params["Especie"][0]
                animales_filtrados = animalesService.filter_animal_by_especi(
                    Especie
                )
                if animales_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, animales_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            
            elif "Género" in query_params:
                Género = query_params["Género"][0]
                animales_filtrados = animalesService.filter_animal_by_genero(
                    Género
                )
                if animales_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, animales_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, animales)
                
                
                
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = animalesService.find_animal(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, [animal])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animales = animalesService.add_student(data)
            HTTPResponseHandler.handle_response(self, 201, animales)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales = animalesService.update_animal(id, data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/animales":
            animales = animalesService.delete_animal()
            HTTPResponseHandler.handle_response(self, 200, animales)
            
            
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = animalesService.delete_animal_id(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, [animal])
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
