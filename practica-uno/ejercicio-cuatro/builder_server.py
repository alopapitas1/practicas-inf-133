from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    def __init__(self):
        self.CI = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_CI(self, CI):
        self.paciente.CI = CI
        return self

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre
        return self

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
        return self

    def set_edad(self, edad):
        self.paciente.edad = edad
        return self

    def set_genero(self, genero):
        self.paciente.genero = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
        return self

    def set_doctor(self, doctor):
        self.paciente.doctor = doctor
        return self

    def build(self):
        return self.paciente

class PacientesService:
    
    pacientes = []
    
    @staticmethod
    def find_paciente(CI):
        return next(
            (paciente for paciente in PacientesService.pacientes if paciente.CI == CI),
            None,
        )
        
    @staticmethod
    def delete_paciente(CI):
        for paciente in PacientesService.pacientes:
            if paciente.CI == CI:
                PacientesService.pacientes.remove(paciente)
                return paciente  
        return None
        

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in PacientesService.pacientes if paciente.diagnostico == diagnostico
        ]
        
        
    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in PacientesService.pacientes if paciente.doctor == doctor
        ]

    @staticmethod 
    def add_paciente(data):
        paciente = PacienteBuilder() \
            .set_CI(data.get("CI", None)) \
            .set_nombre(data.get("nombre", None)) \
            .set_apellido(data.get("apellido", None)) \
            .set_edad(data.get("edad", None)) \
            .set_genero(data.get("genero", None)) \
            .set_diagnostico(data.get("diagnostico", None)) \
            .set_doctor(data.get("doctor", None)) \
            .build()
        PacientesService.pacientes.append(paciente)
        return paciente

    @staticmethod
    def update_paciente(CI, data):
        paciente = PacientesService.find_paciente(CI)
        if paciente:
            for key, value in data.items():
                setattr(paciente, key, value)
            return paciente
        else:
            return None

    @staticmethod
    def delete_pacientes():
        PacientesService.pacientes.clear()
        return PacientesService.pacientes


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

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(diagnostico)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
                    
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(doctor)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
                
            else:
                HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__ for paciente in PacientesService.pacientes])
                
        elif self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            paciente = PacientesService.find_paciente(CI)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            paciente = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, paciente.__dict__)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            data = self.read_data()
            paciente = PacientesService.update_paciente(CI, data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/pacientes":
            pacientes = PacientesService.delete_pacientes()
            HTTPResponseHandler.handle_response(self, 200, {"message": "Todos los pacientes han sido eliminados"})
        elif self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            paciente = PacientesService.delete_paciente(CI)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
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
