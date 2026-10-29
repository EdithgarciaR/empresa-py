# notebook/limpieza/limpieza.py
import pandas as pd
from notebook.exportacion.exportacion_empresa import CARPETA_CRUDOS, CARPETA_LIMPIOS, NOMBRE_ENTIDAD

# Valores válidos
SECTORES = ["textiles", "industriales", "tecnologicos", "salud", "turismo"]

# Funciones base 

def verificar_dato_vacio(dato):
    if pd.isna(dato):
        return True
    return str(dato).strip() == ""   # corregido: faltaba comparar con ==

# Limpieza por campo 

# nombre (texto)
def limpiar_nombre(nombre):
    if verificar_dato_vacio(nombre):
        return None
    return nombre.strip().title()

# nit (texto) → dejar solo dígitos y dígito de verificación: "9001234567-1"
def limpiar_nit(nit):
    if verificar_dato_vacio(nit):
        return None
    solo_digitos = ''.join(c for c in str(nit) if c.isdigit())
    if len(solo_digitos) < 10:
        return None
    cuerpo, dv = solo_digitos[:9], solo_digitos[9]
    return f"{cuerpo}-{dv}"

# sector (texto)
def limpiar_sector(sector):
    if verificar_dato_vacio(sector):
        return None
    sector_limpio = sector.strip().lower()
    if sector_limpio not in SECTORES:
        return None
    return sector_limpio

# contacto (texto)
def limpiar_contacto(contacto):
    if verificar_dato_vacio(contacto):
        return None
    return contacto.strip().title()

# correo (texto)
def limpiar_correo(correo):
    if verificar_dato_vacio(correo):
        return None
    correo = correo.strip().lower()
    if "@" not in correo:          # correos inválidos (suciedad aplicada)
        return None
    return correo

# telefono (texto) → dejar solo 10 dígitos: "3001234567"
def limpiar_telefono(telefono):
    if verificar_dato_vacio(telefono):
        return None
    solo_digitos = ''.join(c for c in str(telefono) if c.isdigit())
    if len(solo_digitos) < 10:
        return None
    return solo_digitos[-10:]      # toma los últimos 10 (descarta el 57 del +57)

# activo (booleano)
def limpiar_activo(activo):
    if verificar_dato_vacio(activo):
        return None
    if activo in [True, "SI", "Si", "sí", "si", "1", 1]:
        return True
    if activo in [False, "NO", "No", "no", "0", 0]:
        return False
    return None

# Función principal 

def limpiar_datos(datos_df):
    datos_df = datos_df.copy()

    datos_df["nombre"]   = datos_df["nombre"].map(limpiar_nombre)
    datos_df["nit"]      = datos_df["nit"].map(limpiar_nit)
    datos_df["sector"]   = datos_df["sector"].map(limpiar_sector)
    datos_df["contacto"] = datos_df["contacto"].map(limpiar_contacto)
    datos_df["correo"]   = datos_df["correo"].map(limpiar_correo)
    datos_df["telefono"] = datos_df["telefono"].map(limpiar_telefono)
    datos_df["activo"]   = datos_df["activo"].map(limpiar_activo)

    return datos_df