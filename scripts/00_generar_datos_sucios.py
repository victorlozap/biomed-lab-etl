import pandas as pd
from faker import Faker
import random
import os

# 1. Configuración Inicial
fake = Faker('es_ES')  # Generador de datos en español
NUM_REGISTROS = 50

# Aseguramos que existan las carpetas
os.makedirs('data/raw', exist_ok=True)

print("🏥 Generando datos biomédicos simulados (y sucios)...")

# --- SEDE CENTRAL (Formato .CSV, bastante limpio) ---
# Estándar: id_paciente | fecha_toma | glucosa_mg_dl
data_central = []
for _ in range(NUM_REGISTROS):
    data_central.append({
        'id_paciente': fake.ssn(),  # Cédula simulada
        'fecha_toma': fake.date_this_year(),
        'glucosa_mg_dl': random.randint(70, 140) # Rangos normales y pre-diabetes
    })

df_central = pd.DataFrame(data_central)
df_central.to_csv('data/raw/reporte_central_2024.csv', index=False)
print("✅ Sede Central: CSV generado.")


# --- SEDE NORTE (Formato .Excel, nombres de columnas distintos) ---
# Problema: Usan "Glucose Level" en inglés y la fecha tiene hora
data_norte = []
for _ in range(NUM_REGISTROS):
    data_norte.append({
        'Patient_ID': fake.ssn(),
        'Sample_Date': fake.date_time_this_year(),
        'Glucose Level': random.randint(65, 180) # Incluye algunos valores altos
    })

df_norte = pd.DataFrame(data_norte)
df_norte.to_excel('data/raw/reporte_sede_norte.xlsx', index=False)
print("✅ Sede Norte: Excel generado (con esquema diferente).")


# --- SEDE SUR (Formato .JSON, datos muy sucios) ---
# Problema: La glucosa viene como texto ("100 mg/dL") y hay nulos
data_sur = []
for _ in range(NUM_REGISTROS):
    # Simulamos un error humano: 10% de veces no registran glucosa
    glucosa = f"{random.randint(60, 300)} mg/dL" if random.random() > 0.1 else None
    
    data_sur.append({
        'paciente_id': fake.ssn(),
        'timestamp': str(fake.date_time_this_year()),
        'resultado_glucosa': glucosa
    })

df_sur = pd.DataFrame(data_sur)
# JSON orientado a registros es común en APIs médicas
df_sur.to_json('data/raw/data_raw_sur.json', orient='records')
print("✅ Sede Sur: JSON generado (con formatos de texto y nulos).")

print("\n🎉 ¡Datos listos en la carpeta 'data/raw'!")