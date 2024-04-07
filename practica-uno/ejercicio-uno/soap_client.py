from zeep import Client

client = Client('http://localhost:8000')

def operacion(a1,b1,opera):
    ope_dis={
        "sumar": client.service.SUMA,
        "restar": client.service.RESTA,
        "multiplicar": client.service.MULTIPLICACION,
        "dividir": client.service.DIVISION,
        }
    
    result=ope_dis[opera](a=a1,b=b1)
    print("El resultado de la operacion es: ",result)


#operaciones 
#suma,resta,multiplicar,dividir

operacion(4,2,"sumar")
operacion(4,2,"restar")
operacion(4,2,"multiplicar")
operacion(4,2,"dividir")
