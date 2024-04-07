from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler


def suma(a,b):
    return a+b 

def resta(a,b):
    return a-b 

def multiplicacion(a,b):
    return a*b 

def division(a,b):
    return float( a/b )


dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)



dispatcher.register_function(
    "SUMA",suma,returns={"sumar": int},
    args={"a": int, "b":int},
)

dispatcher.register_function(
    "RESTA",
    resta,
    returns={"restar": int},
    args={"a": int, "b":int},
)

dispatcher.register_function(
    "MULTIPLICACION",
    multiplicacion,
    returns={"multiplicar": int},
    args={"a": int, "b":int},
)

dispatcher.register_function(
    "DIVISION",
    division,
    returns={"dividir": float},
    args={"a": int, "b":int},
)


# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
