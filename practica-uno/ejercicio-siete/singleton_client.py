import requests


url = "http://localhost:8000/"


print("1----------------------------------------")
ruta_get = url + "partidas"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("2----------------------------------------")
ruta_post = url + "partidas"
nueva_partida = {
    "elemento_jugador": "tijera"
}
post_response = requests.request(method="POST", url=ruta_post, json=nueva_partida)
print(post_response.text)
print("3----------------------------------------")
ruta_post = url + "partidas"
nueva_partida = {
    "elemento_jugador": "piedra"
}
post_response = requests.request(method="POST", url=ruta_post, json=nueva_partida)
print(post_response.text)
print("4----------------------------------------")
ruta_post = url + "partidas"
nueva_partida = {
    "elemento_jugador": "piedra"
}
post_response = requests.request(method="POST", url=ruta_post, json=nueva_partida)
print(post_response.text)



ruta_get = url + "partidas?resultado=gano"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

