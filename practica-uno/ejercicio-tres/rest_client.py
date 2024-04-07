import requests

url = "http://localhost:8000/"

print("1-------------------------------------")

ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("2-------------------------------------")

ruta_post = url + "pacientes"
nuevo_estudiante = {
    "CI": "2",
    "nombre": "maria",
    "apellido": "quispe",
    "Edad": "22",
    "Genero":"mujer",
    "Diagnostico":"lesion",
    "Doctor":"Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_estudiante)
print(post_response.text)

print("3-------------------------------------")

ruta_get = url + "pacientes?Diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("4-------------------------------------")
ruta_get_ci = url + "pacientes/2"
get_response = requests.request(method="GET", url=ruta_get_ci)
print(get_response.text)
print("5-------------------------------------")
ruta_delete_stud = url + "pacientes/6"
get_response = requests.request(method="DELETE", url=ruta_delete_stud)
print(get_response.text)

print("6-------------------------------------")

ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("7-------------------------------------")
ruta_get = url + "pacientes?Doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("8-------------------------------------")

ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
