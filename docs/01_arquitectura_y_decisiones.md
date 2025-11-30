# 🏥 Documentación Técnica: Pipeline ETL Biomédico

## 1. Contexto del Negocio
**Problema:** Un laboratorio clínico con 3 sedes descentralizadas genera reportes diarios en formatos no estandarizados (CSV, Excel, JSON). Esto impide la consolidación de información y retrasa la toma de decisiones críticas.

**Objetivo:** Construir un Data Warehouse centralizado que permita la ingesta automática, limpieza y análisis de estos datos en tiempo cercano al real.

---

## 2. Decisiones de Arquitectura

### 🏗️ Contenedorización (Docker)
* **Decisión:** Se utiliza Docker para desplegar la base de datos PostgreSQL.
* **Justificación:** Garantiza que el entorno sea reproducible. Cualquier ingeniero puede clonar el repositorio y levantar la infraestructura con un solo comando (`docker-compose up`), sin lidiar con instalaciones locales o conflictos de versiones.

### 🗄️ Motor de Base de Datos (PostgreSQL)
* **Decisión:** PostgreSQL 13.
* **Justificación:** Elegido por su robustez en tipos de datos y conformidad con estándares SQL. Su capacidad nativa para manejar JSONB lo hace ideal para futuros datos médicos semi-estructurados (como FHIR).

### 🐍 Lenguaje de Orquestación (Python)
* **Decisión:** Python 3.9 + Pandas + SQLAlchemy.
* **Justificación:** Pandas ofrece la mayor flexibilidad para manipulación de dataframes y limpieza de datos sucios. SQLAlchemy abstrae la conexión a base de datos, previniendo inyección SQL y facilitando el mantenimiento.

---

## 3. Estrategia ETL (Extract, Transform, Load)

### Fase 1: Extracción
Se desarrollaron conectores específicos para cada fuente:
1. **Sede Central:** Archivos CSV estructurados.
2. **Sede Norte:** Archivos Excel (.xlsx) con encabezados en inglés.
3. **Sede Sur:** Archivos JSON anidados y con problemas de calidad (texto sucio).

### Fase 2: Transformación (Limpieza)
El pipeline aplica las siguientes reglas de negocio:
* **Normalización de Encabezados:** Todos los campos se renombran al español (`nivel_glucosa`, `fecha_muestra`).
* **Limpieza de Tipos:** Se eliminan unidades de texto (ej: "108 mg/dL" -> 108) para permitir operaciones matemáticas.
* **Manejo de Nulos:** Se descartan registros sin mediciones válidas.
* **Trazabilidad:** Se inyecta la columna `fuente_sede` para auditar el origen del dato.

### Fase 3: Carga
Carga en modo `replace` (para desarrollo) sobre la tabla `hechos_glucosa` en el esquema público de PostgreSQL.

---

## 4. Ejecución y Pruebas
El pipeline se ejecuta mediante el script `01_etl_pipeline.py`, procesando exitosamente lotes de datos sintéticos generados con la librería `Faker`.

---

## 5. Análisis de Resultados (Data Analytics)

Tras la centralización, se ejecutó la siguiente consulta SQL para evaluar la salud poblacional por sede:

```sql
SELECT fuente_sede, ROUND(AVG(nivel_glucosa), 1) as promedio FROM hechos_glucosa GROUP BY fuente_sede;

### 🚨 Hallazgo Crítico
Se detectó una anomalía significativa en la **Sede Sur**, la cual presenta un promedio de glucosa superior a **170 mg/dL**, en contraste con el promedio normal (~100 mg/dL) de las otras sedes. 

**Hipótesis:**
1. Error sistemático en la calibración de los equipos de laboratorio de la Sede Sur.
2. Factor de riesgo epidemiológico en la población de dicha zona geográfica.

**Siguiente paso:** Se recomienda auditoría técnica inmediata a los equipos de la Sede Sur.