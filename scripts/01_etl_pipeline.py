import pandas as pd
from sqlalchemy import create_engine
import os

# --- CONFIGURACIÓN ---
# Cadena de conexión a tu Postgres en Docker
# Formato: postgresql://usuario:contraseña@host:puerto/base_de_datos
DB_CONNECTION_STR = 'postgresql://admin:adminpassword@localhost:5432/biomed_db'
DB_TABLE_NAME = 'hechos_glucosa'

def procesar_sede_central():
    """Procesa el CSV de la Sede Central (El más limpio)"""
    print("🔄 Procesando Sede Central...")
    df = pd.read_csv('data/raw/reporte_central_2024.csv')
    
    # Estandarización de columnas
    df = df.rename(columns={
        'fecha_toma': 'fecha_muestra',
        'glucosa_mg_dl': 'nivel_glucosa'
    })
    
    # Agregar columna de trazabilidad
    df['fuente_sede'] = 'CENTRAL'
    
    # Seleccionar solo las columnas que nos interesan en orden
    return df[['id_paciente', 'fecha_muestra', 'nivel_glucosa', 'fuente_sede']]

def procesar_sede_norte():
    """Procesa el Excel de la Sede Norte"""
    print("🔄 Procesando Sede Norte...")
    df = pd.read_excel('data/raw/reporte_sede_norte.xlsx')
    
    # Normalización
    df = df.rename(columns={
        'Patient_ID': 'id_paciente',
        'Sample_Date': 'fecha_muestra',
        'Glucose Level': 'nivel_glucosa'
    })
    
    df['fuente_sede'] = 'NORTE'
    return df[['id_paciente', 'fecha_muestra', 'nivel_glucosa', 'fuente_sede']]

def procesar_sede_sur():
    """Procesa el JSON sucio de la Sede Sur"""
    print("🔄 Procesando Sede Sur...")
    df = pd.read_json('data/raw/data_raw_sur.json')
    
    # 1. Renombrar
    df = df.rename(columns={
        'paciente_id': 'id_paciente',
        'timestamp': 'fecha_muestra'
    })
    
    # 2. LIMPIEZA CRÍTICA: La glucosa viene como "108 mg/dL" o null
    # Eliminamos nulos primero
    df = df.dropna(subset=['resultado_glucosa'])
    
    # Quitamos el texto " mg/dL" y convertimos a número
    df['nivel_glucosa'] = df['resultado_glucosa'].str.replace(' mg/dL', '').astype(int)
    
    df['fuente_sede'] = 'SUR'
    
    return df[['id_paciente', 'fecha_muestra', 'nivel_glucosa', 'fuente_sede']]

def main():
    print("🚀 Iniciando Pipeline ETL...")
    
    # 1. EXTRACT & TRANSFORM
    df_central = procesar_sede_central()
    df_norte = procesar_sede_norte()
    df_sur = procesar_sede_sur()
    
    # Unir todos los dataframes (Append)
    df_final = pd.concat([df_central, df_norte, df_sur], ignore_index=True)
    
    print(f"📊 Total de registros procesados y limpios: {len(df_final)}")
    
    # 2. LOAD (Carga a Postgres)
    print("💾 Cargando a Base de Datos PostgreSQL...")
    
    # Crear motor de conexión
    engine = create_engine(DB_CONNECTION_STR)
    
    # 'if_exists="replace"' recrea la tabla cada vez que corres el script. 
    # En producción real usaríamos "append".
    df_final.to_sql(DB_TABLE_NAME, engine, index=False, if_exists='replace')
    
    print("✅ ¡Carga Exitosa! Los datos están listos en la tabla 'hechos_glucosa'")

if __name__ == "__main__":
    main()
