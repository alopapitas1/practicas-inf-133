from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs

def calcular_resultado(elemento_jugador, elemento_servidor):
    if elemento_jugador == elemento_servidor:
        return "empato"
    elif (elemento_jugador == "piedra" and elemento_servidor == "tijera") or \
        (elemento_jugador == "tijera" and elemento_servidor == "papel") or \
        (elemento_jugador == "papel" and elemento_servidor == "piedra"):
        return "gano"
    else:
        return "perdio"
    



partidas = [
    {
        "id": 1,
        "elemento_jugador": "piedra",
        "elemento_servidor": random.choice(["piedra","papel","tijera"]),
        "resultado": calcular_resultado("piedra", random.choice(["piedra","papel","tijera"]))
    },
]

class partidasService:
    _instance = None

    @staticmethod
    def get_instance():
        if partidasService._instance is None:
            partidasService._instance = partidasService()
        return partidasService._instance

    def filter_jugador_by_res(self, resultado):
        return [
            jugador for jugador in partidas if jugador["resultado"] == resultado
        ]

    def add_partidas(self, data):
        data["id"] = len(partidas) + 1
        data["resultado"] = calcular_resultado(data["elemento_jugador"], data["elemento_servidor"])
        partidas.append(data)
        return partidas
    
    
    def add_partidas(self, data):
        data["id"] = len(partidas) + 1
        if "elemento_servidor" not in data:
            data["elemento_servidor"] = random.choice(["piedra", "papel", "tijera"])
        data["resultado"] = calcular_resultado(data["elemento_jugador"], data["elemento_servidor"])
        partidas.append(data)
        return partidas

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    partidas_service = partidasService.get_instance()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/partidas":
            if "resultado" in query_params:
                resultado = query_params["resultado"][0]
                partidas_filtrados = self.partidas_service.filter_jugador_by_res(
                    resultado
                )
                if partidas_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, partidas_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, partidas)
        

    def do_POST(self):
        if self.path == "/partidas":
            data = self.read_data()
            partidas = self.partidas_service.add_partidas(data)
            HTTPResponseHandler.handle_response(self, 201, partidas)
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
