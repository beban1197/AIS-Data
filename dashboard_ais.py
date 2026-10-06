import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

# 1. Configuración de la página
st.set_page_config(page_title="AIS Analytics Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Carga de datos optimizada
@st.cache_data
def cargar_datos():
    df = pd.read_csv('/Users/usuario/Documents/ais_data_tratada_2.csv', sep=';')
    # Rellenar nulos para evitar errores de renderizado en ECharts
    for col in ['sog', 'length', 'width', 'cog']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = cargar_datos()

# ==========================================
# BARRA LATERAL: FILTROS INTERACTIVOS
# ==========================================
st.sidebar.header("Filtros Analíticos")

tipos_disponibles = df['shiptype'].dropna().unique().tolist()
tipos_seleccionados = st.sidebar.multiselect(
    "Tipo de Buque:", 
    options=tipos_disponibles, 
    default=tipos_disponibles[:3] if len(tipos_disponibles) > 3 else tipos_disponibles
)

df_filtrado = df[df['shiptype'].isin(tipos_seleccionados)].copy()

sog_max = float(df_filtrado['sog'].max()) if not df_filtrado.empty else 30.0
sog_rango = st.sidebar.slider("Velocidad SOG (kn):", 0.0, float(sog_max), (0.0, float(sog_max)))

len_max = float(df_filtrado['length'].max()) if not df_filtrado.empty else 400.0
len_rango = st.sidebar.slider("Eslora (m):", 0.0, float(len_max), (0.0, float(len_max)))

# Filtro final aplicando todas las condiciones
df_final = df_filtrado[
    (df_filtrado['sog'] >= sog_rango[0]) & (df_filtrado['sog'] <= sog_rango[1]) &
    (df_filtrado['length'] >= len_rango[0]) & (df_filtrado['length'] <= len_rango[1])
].copy()

# Segmentación operativa dinámica
bins_regime = [-1, 8.0, 14.0, 100.0]
labels_regime = ['Maniobra (≤8 kn)', 'Eco-Speed (8–14 kn)', 'Alta Vel. (>14 kn)']
df_final['regime'] = pd.cut(df_final['sog'], bins=bins_regime, labels=labels_regime)

# ==========================================
# PANEL PRINCIPAL
# ==========================================
st.title("🚢 Panel de Control AIS: Inteligencia de Flota")

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Registros Filtrados", f"{len(df_final):,}")
col2.metric("Velocidad Mediana", f"{df_final['sog'].median():.1f} kn" if not df_final.empty else "0 kn")
col3.metric("Eslora Promedio", f"{df_final['length'].mean():.1f} m" if not df_final.empty else "0 m")

st.divider()

# --- FILA 1: Histograma y Donut (ECharts) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribución de Velocidad")
    if not df_final.empty:
        counts, bins = np.histogram(df_final['sog'], bins=15)
        x_labels = [f"{bins[i]:.1f}" for i in range(len(counts))]
        
        opciones_hist = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": x_labels},
            "yAxis": {"type": "value", "splitLine": {"lineStyle": {"color": "#334155", "type": "dashed"}}},
            "series": [{"data": counts.tolist(), "type": "bar", "itemStyle": {"color": "#0ea5e9", "borderRadius": [4, 4, 0, 0]}}]
        }
        st_echarts(options=opciones_hist, height="350px", theme="dark")

with c2:
    st.subheader("Composición Operativa")
    if not df_final.empty:
        regime_counts = df_final['regime'].value_counts().reset_index()
        datos_pie = [{"value": int(row['count']), "name": str(row['regime'])} for _, row in regime_counts.iterrows() if row['count'] > 0]
        
        opciones_pie = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "bottom"},
            "series": [{
                "type": "pie", "radius": ["40%", "70%"],
                "itemStyle": {"borderRadius": 8, "borderColor": '#0e1117', "borderWidth": 3},
                "data": datos_pie,
                "color": ['#3b82f6', '#06b6d4', '#10b981']
            }]
        }
        st_echarts(options=opciones_pie, height="350px", theme="dark")

# --- FILA 2: Dispersión Físico-Operativa (ECharts) ---
st.divider()
st.subheader("Relación Físico-Operativa (Eslora vs Velocidad)")
if not df_final.empty:
    # Preparar datos [Eslora, Velocidad] para el scatter
    datos_scatter = df_final[['length', 'sog']].values.tolist()
    
    opciones_scatter = {
        "tooltip": {
            "trigger": "item", 
            # Uso de sintaxis de plantilla nativa para extraer [x, y] de la lista de datos
            "formatter": "Eslora: {@[0]} m <br/>Velocidad: {@[1]} kn"
        },
        "xAxis": {"name": "Eslora (m)", "type": "value", "splitLine": {"show": False}},
        "yAxis": {"name": "SOG (knots)", "type": "value", "splitLine": {"lineStyle": {"color": "#334155", "type": "dashed"}}},
        "series": [{
            "type": "scatter", 
            "symbolSize": 8, 
            "data": datos_scatter,
            "itemStyle": {"color": "#8b5cf6", "opacity": 0.6}
        }]
    }
    st_echarts(options=opciones_scatter, height="400px", theme="dark")

# --- FILA 3: Grafo de Vínculos Físico Interactivo (ECharts Graph) ---
st.divider()
st.subheader("Red Topológica Operativa (Interactivo)")
st.markdown("Arrastra los nodos para ver las físicas de ECharts en tiempo real.")

if not df_final.empty:
    # Tomar muestra para un rendimiento fluido en navegador (evitando el "Unknown Value")
    df_links = df_final[df_final['navigationalstatus'] != 'Unknown Value'].sample(min(80, len(df_final)), random_state=42)
    
    nodos, links, agregados = [], [], set()
    categorias = [{"name": "MMSI"}, {"name": "Estado"}, {"name": "Tipo"}]
    
    for _, row in df_links.iterrows():
        m = f"ID: {int(row['mmsi'])}"
        e = str(row['navigationalstatus'])
        t = str(row['shiptype'])
        
        if m not in agregados: 
            nodos.append({"name": m, "category": 0, "symbolSize": 10})
            agregados.add(m)
        if e not in agregados: 
            nodos.append({"name": e, "category": 1, "symbolSize": 25})
            agregados.add(e)
        if t not in agregados: 
            nodos.append({"name": t, "category": 2, "symbolSize": 25})
            agregados.add(t)
            
        links.append({"source": m, "target": e})
        links.append({"source": m, "target": t})

    opciones_grafo = {
        "tooltip": {},
        "legend": [{"data": ["MMSI", "Estado", "Tipo"]}],
        "color": ["#0ea5e9", "#e11d48", "#10b981"], # Colores definidos para cada categoría
        "series": [{
            "type": "graph",
            "layout": "force", # Activa el motor de físicas
            "data": nodos,
            "links": links,
            "categories": categorias,
            "roam": True, # Permite hacer zoom y mover el mapa
            "label": {"show": True, "position": "right", "color": "#cbd5e1", "fontSize": 10},
            "force": {"repulsion": 300, "edgeLength": [50, 100]}, # Parámetros de gravedad
            "lineStyle": {"color": "source", "curveness": 0.2, "opacity": 0.4}
        }]
    }
    st_echarts(options=opciones_grafo, height="600px", theme="dark")