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

