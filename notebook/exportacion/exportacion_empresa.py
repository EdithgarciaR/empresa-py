# rutina para generar archivos en diferentes formatos con python
from pathlib import Path

# 1. Configuración general de las rutas
NOMBRE_ENTIDAD = "empresa"
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # Path con P mayúscula
CARPETA_CRUDOS   = CARPETA_PROYECTO / "datos" / "crudos"
CARPETA_LIMPIOS  = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "datos" / "reportes"

# 2. Funciones genéricas para crear los archivos
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, sep=";", index=False)          # index=False: no guarda el índice
    return ruta

def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"  # .json en minúscula
    datos_df.to_json(ruta, orient="records", indent=2)           # indent, no ident
    return ruta

def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, engine="openpyxl")      # index=False
    return ruta

# 3. Exportar datos crudos (tabla sucia)
def exportar_empresas_crudas(datos_df):                  # dos puntos al final
    return [
        exportar_csv  (datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_json (datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_excel(datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
    ]

# 4. Exportar datos limpios (tabla limpia — la usarás después de limpiar)
def exportar_empresas_limpias(datos_df):
    return [
        exportar_csv  (datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_json (datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_excel(datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
    ]

# 5. Punto de entrada
if __name__ == "__main__":
    rutas_crudas = exportar_empresas_crudas(tabla_sucia)
    print("Archivos crudos generados:")
    for r in rutas_crudas:
        print(f"  ✓ {r}")