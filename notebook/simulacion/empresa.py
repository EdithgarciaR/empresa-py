import random
import uuid
import pandas as pd
from faker import Faker

# 1. Escoger el país y el lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Sembrar semillas
Faker.seed(42)
random.seed(42)

# 3. Definir campos:
# id (texto - UUID), nombre (texto), nit (texto), sector (texto),
# contacto (texto), correo (texto), telefono (texto), activo (booleano)

# 4. Definir el número de datos simulados
FILAS = 300
SECTORES = ["textiles", "industriales", "tecnologicos", "salud", "turismo"]

# 5. Construir función generadora de datos
def generar_datos_empresa(numero_registros=FILAS):
    filas = []
    for _ in range(numero_registros):
        filas.append({
            "id":       str(uuid.uuid4()),
            "nombre":   fake.company(),
            "nit":      fake.numerify("#########-#"),
            "sector":   random.choice(SECTORES),
            "contacto": fake.name(),
            "correo":   fake.company_email(),
            "telefono": fake.numerify("3#########"),
            "activo":   random.choice([True, False]),
        })
    return filas

# 6. Organizar en DataFrame
tabla_ordena_empresa = pd.DataFrame(generar_datos_empresa(FILAS))

# 7. Ensuciar los datos

# 7.1 Función para obtener una muestra de índices
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 7.2 Función principal que ensucia los datos
def ensuciar_datos(datos_df):
    datos_df = datos_df.copy()

    # --- nombre ---
    # 10% con espacios sobrantes al inicio y al final
    idx = generar_muestra(datos_df, 0.10)
    datos_df.loc[idx, "nombre"] = " " + datos_df.loc[idx, "nombre"] + " "

    # 15% en MAYÚSCULAS
    idx = generar_muestra(datos_df, 0.15)
    datos_df.loc[idx, "nombre"] = datos_df.loc[idx, "nombre"].str.upper()

    # --- nit ---
    # Mitad con formato 900.123.456-7, mitad sin separadores 9001234567
    idx_nit = generar_muestra(datos_df, 0.50)
    idx_nit_sin = datos_df.index.difference(idx_nit)          # la otra mitad

    def formatear_nit_puntos(nit):
        # nit original tiene forma "#########-#"  (9 dígitos + guión + 1 dígito)
        digitos = nit.replace("-", "")                         # 10 dígitos
        cuerpo, dv = digitos[:9], digitos[9]
        return f"{cuerpo[:3]}.{cuerpo[3:6]}.{cuerpo[6:]}-{dv}"

    def formatear_nit_plano(nit):
        return nit.replace("-", "")                            # sin guión ni puntos

    datos_df.loc[idx_nit, "nit"] = datos_df.loc[idx_nit, "nit"].map(formatear_nit_puntos)
    datos_df.loc[idx_nit_sin, "nit"] = datos_df.loc[idx_nit_sin, "nit"].map(formatear_nit_plano)

    # --- sector ---
    def escribir_mal(texto):
        variantes = [texto.capitalize(), texto.upper(), f" {texto.lower()} "]
        return random.choice(variantes)

    idx = generar_muestra(datos_df, 0.20)
    datos_df.loc[idx, "sector"] = datos_df.loc[idx, "sector"].map(escribir_mal)

    # --- contacto ---
    # 8% en None (nulos)
    idx = generar_muestra(datos_df, 0.08)
    datos_df.loc[idx, "contacto"] = None

    # --- correo ---
    # 6% sin arroba (correo inválido)
    idx = generar_muestra(datos_df, 0.06)
    datos_df.loc[idx, "correo"] = datos_df.loc[idx, "correo"].str.replace("@", "", regex=False)

    # --- telefono ---
    # Tres formatos: '3001234567', '300 123 4567', '+57 300-123-4567'
    def formatear_telefono(tel, formato):
        t = str(tel)                                           # '3XXXXXXXXX' (10 dígitos)
        if formato == 0:
            return t                                           # sin cambios
        elif formato == 1:
            return f"{t[:3]} {t[3:6]} {t[6:]}"               # '300 123 4567'
        else:
            return f"+57 {t[:3]}-{t[3:6]}-{t[6:]}"           # '+57 300-123-4567'

    # Asignar un formato aleatorio a cada fila
    datos_df["telefono"] = datos_df["telefono"].apply(
        lambda tel: formatear_telefono(tel, random.choice([0, 1, 2]))
    )

    # --- activo ---
    # 15% como texto: 'SI', 'No', '1', '0'
    def escribir_activa(valor):
        opciones = ["SI", "No", "1", "0"]
        return random.choice(opciones)

    idx = generar_muestra(datos_df, 0.15)
    datos_df["activo"] = datos_df["activo"].astype(object)    # permite tipos mixtos
    datos_df.loc[idx, "activo"] = datos_df.loc[idx, "activo"].map(escribir_activa)

    return datos_df

# 8. Aplicar la función
tabla_sucia = ensuciar_datos(tabla_ordena_empresa)

# 9. Verificar resultados
print(tabla_sucia.shape)
print(tabla_sucia.dtypes)
print(tabla_sucia.head(10).to_string())