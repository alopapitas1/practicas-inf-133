import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los animales por la ruta /animales

print("1----------------------------------------")
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo estudiante por la ruta /animales
print("2----------------------------------------")
ruta_post = url + "animales"
nuevo_animal = {
    "id": 2,
    "nombre": "condor",
    "Especie": "ave",
    "Género": "hembra",
    "Edad":"11",
    "Peso": "9"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

print("3----------------------------------------")
# GET filtrando por nombre con query params
ruta_get = url + "animales?Especie=ave"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("4----------------------------------------")
ruta_get = url + "animales?Género=macho"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("5----------------------------------------")
ruta_put = url + "animales/2"
animal_actualizado = {
    "id": 2,
    "nombre": "condor",
    "Especie": "ave",
    "Género": "hembra",
    "Edad":"22",
    "Peso": "31"
}
post_response = requests.request(method="PUT", url=ruta_put, json=animal_actualizado)
print(post_response.text)

print("6----------------------------------------")

ruta_delete = url + "animales/1"
get_response = requests.request(method="DELETE", url=ruta_delete)
print(get_response.text)

print("7----------------------------------------")
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
