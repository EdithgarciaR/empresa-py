import random
import uuid

from faker import Faker

#1 Escoger el pais y el lenguaje para simular los datos
fake=Faker("es_CO")

#2 Sembrar semillas
Faker.seed(42)
random.seed(42)

#Definir 
#id (texto) (UUDI)
#nombre (texto)
#nit (texto)
#sector (texto)
#contacto (texto)
#Correo (texto)
#telefono (texto)
#activo (booleano)


#4 Definir el numero de datos simulados(DATASET)
FILAS=300

SECTORES=["textiles", "industriales", "tecnologicos","salud", "turismo"]

#5 construir funcion generadora de los datos 

def generar_datos_empresa(numero_registros=FILAS):
    filas=[]


    for _ in range(numero_registros):
         filas.append({
        "id":str(uuid.uuid4()),
        "nombre":fake.company(),
        "nit":fake.numerify("#########-#"),
        "sector":random.choice(SECTORES),
        "contacto":fake.name(),
        "correo":fake.company_email(),
        "telefono":fake.numerify("3#########"),
        "activo":random.choice([True, False]),
     
    })

    return filas
