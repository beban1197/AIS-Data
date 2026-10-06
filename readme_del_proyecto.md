# 🚢 AIS Analytics Pro: Inteligencia de Flota Marítima

Este repositorio contiene un panel de control interactivo (Dashboard) diseñado para analizar y visualizar datos del Sistema de Identificación Automática (AIS) de embarcaciones marítimas. La aplicación transforma datos de telemetría en bruto en inteligencia operativa procesable mediante visualizaciones dinámicas y físicas en tiempo real.

## 🎯 Objetivo del Proyecto

Demostrar la capacidad de procesar bases de datos marítimas, limpiar anomalías de transmisión (como los clústeres de "Unknown Values") y desplegar una arquitectura de Business Intelligence (BI) de grado empresarial. La interfaz permite explorar la relación entre las dimensiones físicas de los buques y su comportamiento operativo.

## ✨ Características Principales

- **Filtros Analíticos Dinámicos:** Segmentación de la flota en tiempo real por tipo de buque, eslora (m) y velocidad sobre el fondo (SOG).
- **Motor Gráfico Avanzado (Apache ECharts):**
  - **Red Topológica Operativa:** Grafo interactivo con motor de físicas (*force layout*) que mapea la relación entre identificadores (MMSI), tipo de buque y estado de navegación.
  - **Dispersión Físico-Operativa:** Gráfico interactivo con *tooltips* nativos que correlacionan el tamaño de la embarcación con su régimen de velocidad.
  - **Distribución y Composición:** Histogramas y gráficos de anillo (Donut) para clasificar maniobras (Eco-Speed, Alta Velocidad, etc.).
- **Datos Depurados:** Pipeline integrado con Pandas para el manejo de valores nulos y normalización de variables.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.9+
- **Framework Web:** Streamlit
- **Manipulación de Datos:** Pandas, NumPy
- **Visualización:** `streamlit-echarts` (Apache ECharts)

## 🚀 Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/beban1197/AIS-Data.git
   cd AIS-Data
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv entorno_ais
   source entorno_ais/bin/activate  # En Mac/Linux
   # entorno_ais\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install streamlit pandas numpy streamlit-echarts
   ```

4. **Ejecutar la aplicación:**
   ```bash
   streamlit run dashboard_ais.py
   ```

## 🧠 Insights Generados
El análisis de estos datos permite identificar cuellos de botella en las operaciones portuarias, perfilar el comportamiento por industria (Carga, Pesca, Servicios) y aislar fallas sistemáticas en la transmisión de transpondedores AIS de flotas específicas.