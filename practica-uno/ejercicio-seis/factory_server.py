from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "genero": self.genero,
            "edad": self.edad,
            "peso": self.peso
        }


class AnimalFactory:
    @staticmethod
    def create_animal(id, nombre, especie, genero, edad, peso):
        return Animal(id, nombre, especie, genero, edad, peso)

class AnimalService:
    animales = []

    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in AnimalService.animales if animal.id == id),
            None,
        )

    @staticmethod
    def filter_animal_by_especie(especie):
        return [
            animal for animal in AnimalService.animales if animal.especie == especie
        ]

    @staticmethod
    def filter_animal_by_genero(genero):
        return [
            animal for animal in AnimalService.animales if animal.genero == genero
        ]

    @staticmethod
    def add_animal(data):
        animal = AnimalFactory.create_animal(**data)
        AnimalService.animales.append(animal)
        return animal

    @staticmethod
    def update_animal(id, data):
        animal = AnimalService.find_animal(id)
        if animal:
            for key, value in data.items():
                setattr(animal, key, value)
            return animal
        else:
            return None

    @staticmethod
    def delete_animal():
        AnimalService.animales.clear()
        return AnimalService.animales

    @staticmethod
    def delete_animal_id(id):
        for animal in AnimalService.animales:
            if animal.id == id:
                AnimalService.animales.remove(animal)
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
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = AnimalService.filter_animal_by_especie(especie)
                if animales_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = AnimalService.filter_animal_by_genero(genero)
                if animales_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, [vars(animal) for animal in AnimalService.animales])
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = AnimalService.find_animal(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, vars(animal))
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            content_length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            animal = AnimalService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, vars(animal))
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            animal = AnimalService.update_animal(id, data)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, vars(animal))
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/animales":
            animales = AnimalService.delete_animal()
            HTTPResponseHandler.handle_response(self, 200, animales)
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = AnimalService.delete_animal_id(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, vars(animal))
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

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
