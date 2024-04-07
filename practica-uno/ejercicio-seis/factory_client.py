import requests
import json

# Definimos la URL base del servidor
base_url = "http://localhost:8000/animales"

# Definimos los encabezados HTTP que vamos a enviar con las peticiones
headers = {"Content-Type": "application/json"}
print("1-----------------------------------------------")

# Crear un animal
response = requests.post(base_url, json={
    "id": 1,
    "nombre": "León",
    "especie": "Felino",
    "genero": "Macho",
    "edad": "7",
    "peso": "180"
}, headers=headers)
print("Respuesta del servidor al crear un animal:", response.json())

print("2-----------------------------------------------")
# Listar todos los animales
response = requests.get(base_url)
print("Respuesta del servidor al listar todos los animales:", response.json())

print("3-----------------------------------------------")
# Buscar animales por especie
response = requests.get(f"{base_url}?especie=Felino")
try:
    json_response = response.json()
    print("Respuesta del servidor al buscar animales por especie:", json_response)
except json.decoder.JSONDecodeError:
    print("Respuesta del servidor al buscar animales por especie:", response.text)

print("4-----------------------------------------------")
# Buscar animales por género
response = requests.get(f"{base_url}?genero=Macho")
try:
    json_response = response.json()
    print("Respuesta del servidor al buscar animales por genero:", json_response)
except json.decoder.JSONDecodeError:
    print("Respuesta del servidor al buscar animales por genero:", response.text)

print("5-----------------------------------------------")
# Actualizar la información de un animal
response = requests.put(f"{base_url}/1", json={"edad": "8"}, headers=headers)
print("Respuesta del servidor al actualizar la información de un animal:", response.json())

print("6-----------------------------------------------")
# Eliminar un animal
response = requests.delete(f"{base_url}/1")
print("Respuesta del servidor al eliminar un animal:", response.json())
