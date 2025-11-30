# 🏥 Pipeline ETL de Normalización de Datos Clínicos

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Postgres](https://img.shields.io/badge/Postgres-13-336791)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📋 Descripción del Proyecto
Este proyecto implementa una solución de **Ingeniería de Datos** para resolver un problema de fragmentación de información en un entorno hospitalario.

Se simula un escenario donde 3 sedes clínicas reportan resultados de laboratorio en formatos heterogéneos (CSV, Excel, JSON "sucia"). El objetivo es ingestar, normalizar y centralizar estos datos en un **Data Warehouse (PostgreSQL)** para permitir análisis clínicos unificados y detección de anomalías.

### 🎯 Objetivos Técnicos
* **Ingesta Multi-fuente:** Procesamiento de archivos planos y semi-estructurados.
* **Calidad de Datos:** Limpieza de valores nulos, estandarización de unidades de medida (mg/dL) y normalización de esquemas.
* **Infraestructura como Código:** Despliegue de base de datos utilizando contenedores Docker para garantizar reproducibilidad.

## 🏗️ Arquitectura y Tech Stack

* **Lenguaje:** Python 3.9 (Pandas, SQLAlchemy, Faker).
* **Base de Datos:** PostgreSQL 13 (Corriendo en Docker).
* **Contenedorización:** Docker & Docker Compose.
* **Orquestación:** Scripts modulares de Python.

---

## 📂 Estructura del Proyecto

```bash
biomed-lab-etl/
├── data/
│   └── raw/                   # Landing zone para archivos crudos (CSV, XLSX, JSON)
├── docs/                      # Documentación de arquitectura y decisiones
├── pg_data/                   # Persistencia de datos de Postgres (Ignorado por Git)
├── scripts/
│   ├── 00_generar_datos_sucios.py   # Generador de data sintética (Faker)
│   └── 01_etl_pipeline.py           # Script principal ETL
├── docker-compose.yml         # Definición de infraestructura
└── requirements.txt           # Dependencias de Python
```


## 🚀 Guía de Instalación y Ejecución

Si deseas replicar este proyecto en tu entorno local, sigue estos pasos:

### 1. Prerrequisitos
* **Docker Desktop** instalado y ejecutándose.
* **Python 3.8+** instalado.
* **Git** instalado.

### 2. Clonar el repositorio e instalar dependencias
```bash
git clone [https://github.com/TU_USUARIO/biomed-lab-etl.git](https://github.com/TU_USUARIO/biomed-lab-etl.git)
cd biomed-lab-etl
```

# Se recomienda usar entorno virtual
pip install pandas sqlalchemy psycopg2-binary faker openpyxl


### 3. Despliegue de Infraestructura (Base de Datos)
Ejecutar el contenedor de Docker que levantará la instancia de PostgreSQL.
```bash
docker-compose up -d
```

### 4. Ejecución del Pipeline
El proyecto incluye un generador de datos para simular el entorno hospitalario.

**Paso A: Generar datos de prueba**
```bash
python scripts/00_generar_datos_sucios.py
```

**Paso B: Correr el proceso ETL**
```bash
python scripts/01_etl_pipeline.py
```

## 📊 Resultados e Impacto
Tras la ejecución del pipeline y el análisis de los datos centralizados, se identificó un **hallazgo crítico**:

> 🚨 **Anomalía Detectada:** La **Sede Sur** presenta un promedio de glucosa de **177.5 mg/dL**, significativamente superior al promedio de la Sede Central (101.3 mg/dL).

Esta discrepancia, visible solo tras la unificación de los datos, sugiere una posible descalibración en los equipos de medición de dicha sede o un factor de riesgo poblacional no atendido.

---

## 👤 Autor
**Victor Lopez**
*Ingeniero Biomédico & Analytics Engineer*