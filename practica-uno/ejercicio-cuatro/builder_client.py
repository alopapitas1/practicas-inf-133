import requests

BASE_URL = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}


print("1-----------------------------------------------")



nuevo_paciente = {
    "CI": 1234567,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "genero": "hombre",
    "diagnostico": "Hipertensión",
    "doctor": "Pedro Pérez"
}

response = requests.post(BASE_URL, json=nuevo_paciente, headers=headers)
print(response.json())

print("2-----------------------------------------------")

response = requests.get(BASE_URL)

print(response.json())

print("3-----------------------------------------------")

response = requests.get(f"{BASE_URL}/{1234567}")
print(response.json())

print("4-----------------------------------------------")

response = requests.get(f"{BASE_URL}?Diagnostico=Diabetes")
print(response.json())

print("5-----------------------------------------------")

response = requests.get(f"{BASE_URL}?Doctor=Pedro Pérez")
print(response.json())

print("6-----------------------------------------------")

paciente_actualizado = {
    "nombre": "Juan Pablo",
    "edad": 35
}
response = requests.put(f"{BASE_URL}/{1234567}", json=paciente_actualizado, headers=headers)
print(response.json())

print("7-----------------------------------------------")

response = requests.delete(f"{BASE_URL}/{1234567}")
print(response.json())
