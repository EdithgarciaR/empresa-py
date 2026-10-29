import pandas as pd

from notebook.simulacion.empresa import generar_datos_empresa, ensuciar_datos
from notebook.exportacion.exportacion_empresa import exportar_empresas_crudas, exportar_empresas_limpias

# 1. Simulación
print("************ SIMULACIONES DE EMPRESA ************")
empresas_df = pd.DataFrame(generar_datos_empresa())
empresas_sucias_df = ensuciar_datos(empresas_df)

# 2. Exportación
print("************ EXPORTACIONES DE EMPRESA ************")
rutas_crudas = exportar_empresas_crudas(empresas_sucias_df)

print("Archivos crudos generados:")
for ruta in rutas_crudas:
    print(f"  ✓ {ruta}")
