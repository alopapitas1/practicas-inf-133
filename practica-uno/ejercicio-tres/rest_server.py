from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int,Float,Boolean, List, Schema, Field, Mutation


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Float()
    frutos = Boolean()


class Query(ObjectType):
    Plantas = List(Planta)
    Planta_con_frutos = Field(Planta)
    Planta_por_especie = Field(Planta, especie=String())


    def resolve_Plantas(root, info):
        print(Plantas)
        return Plantas
    
    def resolve_Planta_con_frutos(root, info):
        for Planta in Plantas:
            if Planta.frutos == True:
                return Planta
        return None

    def resolve_Planta_por_especie(root, info, especie):
        for Planta in Plantas:
            if Planta.especie == especie:
                return Planta
        return None

class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Float()
        frutos = Boolean()


    Planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nuevo_Planta = Planta(
            id=len(Plantas) + 1, 
            nombre=nombre, 
            especie=especie,
            edad=edad, 
            altura=altura,
            frutos=frutos
        )
        Plantas.append(nuevo_Planta)

        return CrearPlanta(Planta=nuevo_Planta)



class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    Planta = Field(Planta)

    def mutate(root, info, id):
        for i, Planta in enumerate(Plantas):
            if Planta.id == id:
                Plantas.pop(i)
                return DeletePlanta(Planta=Planta)
        return None
    
    
class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Float()
        frutos = Boolean()

    Planta = Field(Planta)

    def mutate(root, info, id, nombre=None, especie=None, edad=None, altura=None, frutos=None):
        for planta in Plantas:
            if planta.id == id:
                if nombre is not None:
                    planta.nombre = nombre
                if especie is not None:
                    planta.especie = especie
                if edad is not None:
                    planta.edad = edad
                if altura is not None:
                    planta.altura = altura
                if frutos is not None:
                    planta.frutos = frutos

                return ActualizarPlanta(Planta=planta)

        return None

    
    

class Mutations(ObjectType):
    crear_Planta = CrearPlanta.Field()
    delete_Planta = DeletePlanta.Field()
    actualizar_Planta=ActualizarPlanta.Field()
    
    
    
Plantas = [
    Planta(
        id=1,
        nombre ="Rosa",
        especie = "roja",
        edad = 4,
        altura = 1.3,
        frutos = True
    ),
    Planta(
        id=2,
        nombre ="clavel",
        especie = "verde",
        edad = 14,
        altura = 4.1,
        frutos = False
    ),
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
