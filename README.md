import random
import uuid
import pandas as pd
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

    #6 utilizamos andas para organizar los atos simulados en un dataframe
   
    tabla_ordena_empresa=pd.DataFrame(generar_datos_empresa(FILAS))

    #.7 Ensuciar los datos

    #1. Genear una funcion que muestre los datos
    
    def generar_muestra(datos,porcentage):
            return datos.sample(frac=porcentage,random_state=random.randint(0,9999)).index
        
    #7.2 Funcion que ensucia los datos
    def ensuciar_datos(datos_df):
            datos_df=datos_df.copy()


    #1.pSe ensucia `nombre`: 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.
    
    subconjunto_datos=generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"]=" "+datos_df.loc[subconjunto_datos,"nombre"]+" "

    subconjunto_datos=generar_muestra(datos_df,0.15)
    datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"].upper()


    #2.Se ensucia `nit`: la mitad con puntos y guiones (900.123.456-7) y la otra mitad sin nada (9001234567).





    #3.Se ensucia `sector`: variantes del mismo sector: 'Logistica', 'LOGISTICA', ' logistica '.
    def escribir_mal(texto):
            variantes=[texto.capitalize(), texto.upper(), f" {texto.lower()} "]
            return random.choice(variantes)

    subconjunto_datos=generar_muestra(datos_df,0.20)
    datos_df.loc[subconjunto_datos,"sector"]=datos_df.loc[subconjunto_datos,"sector"].map(escribir_mal)

    #4. Se ensucia `contacto`: 8% en None (nulos).
    subconjunto_datos=generar_muestra(datos_df,0.08)
    datos_df.loc[subconjunto_datos,"contacto"]=None

    #5.Se ensucia `correo`: 6% sin la arroba (correo invalido).
    subconjunto_datos=generar_muestra(datos_df,0.06)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.replace("@","", regex=False)

    #6.Se ensucia `telefono`: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.





    #7.Se ensucia `activa`: a veces como texto: 'SI', 'No', '1', '0'.
    subconjunto_datos=generar_muestra(datos_df,0.15)
    datos_df["activa"]=datos_df["activa"].astype(object)
    datos_df.loc[subconjunto_datos,"activa"]=datos_df.loc[subconjunto_datos,"activa"].map(escribir_activa)
