import requests


url = "http://localhost:8000/"


print("1-get---------------------------------------")
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)




print("2----------------------------------------")
ruta_post = url + "mensajes"
nuevo_msj = {
    "mensaje":"lobo"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_msj)
print(post_response.text)


ruta_post = url + "mensajes"
nuevo_msj = {
    "mensaje":"Alain"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_msj)
print(post_response.text)

print("3-get---------------------------------------")
ruta_get = url + "mensajes/1"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)



print("4-get---------------------------------------")
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)



print("5----------------------------------------")
ruta_put = url + "mensajes/2"
mensaje_actualizado  = {
    "mensaje": "monito"
}
post_response = requests.request(method="PUT", url=ruta_put, json=mensaje_actualizado )
print(post_response.text)


print("6-get---------------------------------------")
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)



print("7----------------------------------------")

ruta_delete = url + "mensajes/1"
get_response = requests.request(method="DELETE", url=ruta_delete)
print(get_response.text)

print("8----------------------------------------")
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
