# Análisis de Sentimientos y Tweets Políticos

Este repositorio contiene herramientas para el análisis de datos relacionados con tweets políticos en España. Incluye scripts para la limpieza de datos, análisis exploratorio, análisis temporal, modelado de temas (LDA), y análisis de sentimientos utilizando modelos de redes neuronales.

## Contenido del Repositorio

### Archivos Principales
- **`Roses_Nerea_TFM.ipynb`**: Notebook principal con los pasos detallados para limpieza, análisis exploratorio, análisis temporal, modelado de temas y análisis de sentimientos.
- **`json_to_csv.py`**: Script para convertir archivos JSON a CSV.
- **`import asyncio.py`**: Script para realizar scraping de datos desde la API de Bluesky.
- **`import unittest.py`**: Pruebas unitarias para el scraper de Bluesky.
- **`environment.yml`**: Archivo para configurar el entorno conda con las dependencias necesarias.
- **`base_conjunta.csv`**: Archivo CSV que contiene los datos combinados de todos los perfiles políticos.
- **Archivos CSV individuales**: Datos filtrados por perfil político (e.g., `PEDRO SÁNCHEZ_filtered.csv`, `VOX_filtered.csv`).

### Funcionalidades
1. **Limpieza de Datos**: Scripts para filtrar columnas relevantes, eliminar retweets y añadir columnas como `blackout` y `nombre`.
2. **Scraping de Datos**: Obtención de datos desde la API de Bluesky y filtrado por rango de fechas.
3. **Análisis Exploratorio**: Estadísticas descriptivas de los tweets.
4. **Análisis Temporal**: Gráficos de evolución temporal de tweets regulares y relacionados con el apagón.
5. **Modelado de Temas (LDA)**: Identificación de temas principales por perfil político.
6. **Análisis de Sentimientos**: Clasificación de tweets en positivo, negativo y neutral utilizando modelos preentrenados.

## Configuración del Entorno

### Requisitos
- **Python**: Versión 3.9 o superior.
- **Conda**: Para la gestión de entornos.
- **Dependencias**: Listadas en `environment.yml`.

### Instalación
1. **Clonar el repositorio**:
'''   git clone https://github.com/usuario/repositorio.git
   cd repositorio'''

2. **Crear el entorno conda:**
'''conda env create -f environment.yml
conda activate sentimentanal'''

## Ejecución
### Limpieza de Datos
Ejecutar los scripts de limpieza en el notebook Roses_Nerea_TFM.ipynb.

### Scraping de Datos
Ejecutar el script import asyncio.py para obtener datos desde la API de Bluesky:
'''python import asyncio.py
'''
### Análisis Exploratorio
Abrir el notebook Roses_Nerea_TFM.ipynb y ejecutar las celdas correspondientes al análisis exploratorio.

### Análisis Temporal
Ejecutar las celdas del notebook relacionadas con el análisis temporal para generar gráficos de evolución.

### Modelado de Temas
Ejecutar las celdas del notebook relacionadas con el análisis LDA para identificar temas principales.

### Análisis de Sentimientos
Ejecutar las celdas del notebook relacionadas con el análisis de sentimientos para clasificar los tweets.