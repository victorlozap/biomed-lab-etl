# 🏥 Proyecto: Centralización de Datos de Laboratorio (Biomed ETL)

## 1. Contexto del Negocio (El "Por qué")
**Problema:** Un laboratorio clínico tiene 3 sedes. Cada sede genera reportes de exámenes en archivos sucios (Excel/CSV) con formatos distintos. Actualmente, el análisis se hace manual, lo que genera errores y demora la entrega de reportes gerenciales.

**Objetivo:** Crear un repositorio centralizado (Data Warehouse) que ingeste, limpie y estandarice estos datos automáticamente para permitir análisis en tiempo real.

---------

## 2. Decisiones de Arquitectura (El "Cómo" y el "Para qué")

### 🏗️ Decisión 1: Uso de Docker
* **¿Qué es?**: Una herramienta de contenerización.
* **¿Por qué lo usamos?**:
    * **Reproducibilidad:** Evita el problema de "en mi máquina funciona". El entorno es idéntico en desarrollo y producción.
    * **Aislamiento:** No ensuciamos el sistema operativo (Windows) instalando múltiples versiones de bases de datos.
    * **Limpieza:** Si el proyecto falla, borramos el contenedor y el sistema queda intacto.

---------

### 🗄️ Decisión 2: PostgreSQL como Data Warehouse
* **¿Qué es?**: Base de datos relacional (RDBMS) open source.
* **¿Por qué lo elegimos sobre MySQL?**:
    * **Estándar en Data:** Es la base tecnológica de Redshift (AWS) y similar a BigQuery (Google).
    * **Manejo de Datos Complejos:** Mejor soporte nativo para JSON (muy común en formatos médicos como FHIR).
    * **Analítica:** Tiene funciones de ventana (Window Functions) más robustas para análisis estadístico.

---------

### 🐍 Decisión 3: Python como Motor de Ingesta
* **¿Qué es?**: Lenguaje de programación de propósito general.
* **¿Por qué lo usamos?**:
    * **Ecosistema de Datos:** Librerías como `Pandas` son el estándar de oro para manipulación tabular.
    * **Conectividad:** `SQLAlchemy` permite interactuar con bases de datos (SQL) usando objetos de Python, abstrayendo la complejidad de SQL puro.
    * **Faker:** Usaremos la librería `Faker` para generar datos sintéticos que simulan información de pacientes (PII) sin comprometer datos reales, cumpliendo normas éticas (HIPAA/GDPR).

---------

## 3. Estrategia de Transformación (ETL)

El desafío es unificar 3 fuentes con esquemas distintos en una **Tabla Maestra**.

### Esquema de Salida (Target Schema)
Independientemente de cómo llegue el dato, en nuestra base de datos (Postgres) se guardará siempre con este formato estándar:

| Columna | Tipo SQL | Descripción |
| :--- | :--- | :--- |
| `id_paciente` | TEXT | Identificador único del paciente (anónimo) |
| `fecha_muestra` | TIMESTAMP | Fecha y hora estandarizada de la toma |
| `nivel_glucosa` | INTEGER | Valor numérico limpio (sin texto "mg/dL") |
| `fuente_sede` | TEXT | Para trazabilidad (Saber de qué archivo vino) |

### Reglas de Limpieza
1. **Sede Norte (Excel):** Renombrar `Glucose Level` -> `nivel_glucosa`.
2. **Sede Sur (JSON):** Eliminar la unidad de medida " mg/dL" del texto y convertir a número. Manejar valores nulos (descartar o marcar).

---------

## 4. Implementación del Pipeline ETL

### Tecnología Utilizada
Se construyó un script en Python (`01_etl_pipeline.py`) que actúa como orquestador del flujo de datos.

### Fases del Proceso
#### 1. Extracción (Extract)
* Se utilizan conectores específicos de Pandas para cada formato:
    * `read_csv` para Sede Central.
    * `read_excel` (motor openpyxl) para Sede Norte.
    * `read_json` para Sede Sur.

#### 2. Transformación (Transform)
Se aplica **lógica de negocio** para normalizar los datos antes de que toquen la base de datos:
* **Estandarización de Esquema:** Se renombran columnas dispares (`Glucose Level`, `resultado_glucosa`) al estándar `nivel_glucosa`.
* **Limpieza de Datos (Data Cleaning):**
    * En la Sede Sur, se eliminan sufijos de texto (" mg/dL") para convertir el campo a numérico (`Integer`).
    * Se eliminan registros nulos que no aportan valor clínico.
* **Enriquecimiento:** Se agrega la columna `fuente_sede` para mantener la trazabilidad del dato (Data Lineage).

#### 3. Carga (Load)
* Se utiliza `SQLAlchemy` para crear una conexión segura con el contenedor Docker.
* Modo de carga: `if_exists='replace'` (para desarrollo/pruebas). En producción se cambiaría a `'append'` (incremental).

### Resultado
* **Input:** 3 archivos heterogéneos y sucios.
* **Output:** Tabla `hechos_glucosa` en PostgreSQL con esquema unificado y tipos de datos correctos.