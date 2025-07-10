import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import plotly.graph_objects as go

# Configuración de la página y estilo
st.set_page_config(
    page_title="Dashboard Seguimiento al Electorado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR con imagen del candidato y logo ---
with st.sidebar:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQO1NDVDVWs0FTPlUoBjM-3SLomQrL0ajkbCQ&s",
        use_container_width=True
    )
    st.markdown("""
        <div style='font-size:14px; font-style:italic; color:#2c3e50; margin-top:10px;'>
        "Porque Salas se gobierna con la cabeza pero sobre todo... con el corazón" 💛
        </div>
        <div style='font-size:15px; font-weight:bold; margin-top:8px; color:#34495e;'>
        Ing. Edward Romero.
        </div>
        <hr style='margin-top:15px;'>
        <div style='font-size:13px; color:#7f8c8d;'>
        Campaña Política Digital 2026- Salas
        </div>
    """, unsafe_allow_html=True)

# --- HEADER con estilo ---
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 20px;
        color: #34495e;
        margin-top: 0;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">📊 Dashboard Seguimiento al Electorado - Salas</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Distrito Salas Guadalupe - Campaña 2026</p>', unsafe_allow_html=True)

# --- Datos ficticios con flag primer voto ---
data = {
    "Anexo": ["Guadalupe", "Villacurí", "Punta Hermosa", "Cerro Prieto", "Collazos",
              "Expansión Urbana", "Villa Rotari", "Camino de Reyes"],
    "Votantes": [3995, 3075, 2758, 2678, 2275, 1857, 1262, 898],
    "% Jóvenes (18-25)": [40, 30, 35, 25, 20, 30, 40, 30],
    "% Adultos (26-59)": [45, 55, 50, 60, 65, 55, 50, 55],
    "% Adultos mayores (60+)": [15, 15, 15, 15, 15, 15, 10, 15],
    "% Primer Voto (17-21)": [16, 12, 14, 10, 8, 12, 16, 12],
    # Datos nuevos de género:
    "% Varones": [52, 48, 50, 47, 49, 51, 53, 50],   # Ejemplo, suma siempre 100% varones + mujeres
}

df = pd.DataFrame(data)
df["% Mujeres"] = 100 - df["% Varones"]

# --- Cálculo de segmentos ---
df["Primer Voto"] = df["Votantes"] * df["% Primer Voto (17-21)"] / 100
df["Jóvenes (18-25)"] = df["Votantes"] * df["% Jóvenes (18-25)"] / 100 - df["Primer Voto"]
df["Adultos (26-59)"] = df["Votantes"] * df["% Adultos (26-59)"] / 100
df["Adultos mayores (60+)"] = df["Votantes"] * df["% Adultos mayores (60+)"] / 100
total_votantes = df["Votantes"].sum()

# --- Métrica total de votantes ---
st.markdown("### 🧮 Cantidad Total de Votantes")
st.markdown(f'<div style="font-size:36px; font-weight:bold; color:#2ecc71; margin-bottom:30px;">{total_votantes:,}</div>', unsafe_allow_html=True)

# --- Gráfico votos ganador vs total votantes activos histórico ---
anios = [2006, 2010, 2014, 2018, 2022, 2026]
total_votantes_hist = [7963, 9740, 11015, 12215, 13908, 15997]

random.seed(42)  # Para reproducibilidad
votos_ganador_hist = [2521,2110,2443,3365,3443,4144]
votos_otros_hist = [tv - vg for tv, vg in zip(total_votantes_hist, votos_ganador_hist)]

# Calcular porcentajes
pct_ganador = [vg * 100 / tv for vg, tv in zip(votos_ganador_hist, total_votantes_hist)]
pct_otros = [100 - pg for pg in pct_ganador]

# Customdata para tooltip: votos_otros y total votos
customdata = np.array([votos_otros_hist, total_votantes_hist]).T

fig_hist = go.Figure()

# Barras votos ganador
fig_hist.add_trace(go.Bar(
    x=anios,
    y=votos_ganador_hist,
    name='Votos Ganador',
    marker_color='royalblue',
    text=[f'{p:.1f}%' for p in pct_ganador],  # Texto % dentro barra
    textposition='inside',
    insidetextanchor='middle',
    hovertemplate=(
        "<b>Año: %{x}</b><br>" +
        "Votos Ganador: %{y}<br>" +
        "Otros Votos: %{customdata[0]}<br>" +
        "<b>Total Votos Emitidos: %{customdata[1]}</b><extra></extra>"
    ),
    customdata=customdata
))

# Barras otros votos
fig_hist.add_trace(go.Bar(
    x=anios,
    y=votos_otros_hist,
    name='Otros Votos',
    marker_color='lightgray',
    text=[f'{p:.1f}%' for p in pct_otros],
    textposition='inside',
    insidetextanchor='middle',
    hoverinfo='skip'
))

fig_hist.update_layout(
    barmode='stack',
    xaxis_title='Año',
    yaxis_title='Número de Votantes',
    template='plotly_white',
    height=450,
    legend=dict(y=0.98, x=0.02),
    margin=dict(t=30, b=40, l=40, r=40)
)

# Aquí pones el título con emoji y estilo usando st.subheader antes del gráfico:
st.subheader("🏆 Tendencia Histórica Voto Ganador vs. Voto Emitido y Estimación 2026")
config = {
    'scrollZoom': False,       # Desactiva zoom con scroll
    'displayModeBar': False,   # Oculta la barra de herramientas
    'staticPlot': False         # Hace el gráfico estático, sin interacciones
}

st.plotly_chart(fig_hist, use_container_width=True, config=config)

# --- Tabla de datos ---
st.subheader("📋 Datos segmentados por anexo")
st.dataframe(
    df[["Anexo", "Votantes", "Primer Voto", "Jóvenes (18-25)", "Adultos (26-59)", "Adultos mayores (60+)", "% Varones", "% Mujeres"]].astype({"Primer Voto": int, "Jóvenes (18-25)": int, "Adultos (26-59)": int, "Adultos mayores (60+)": int})
)

# --- Gráficos en vertical y orden cambiado ---

# 1) Composición total grupos etarios
st.subheader("🧑‍🤝‍🧑 Composición por Grupos de Edad")
total_primervoto = df["Primer Voto"].sum()
total_jovenes = df["Jóvenes (18-25)"].sum()
total_adultos = df["Adultos (26-59)"].sum()
total_mayores = df["Adultos mayores (60+)"].sum()

colors_etarios = {
    "Primer Voto": "#0072B2",          # Azul vibrante
    "Jóvenes (18-25)": "#009E73",     # Verde azulado
    "Adultos (26-59)": "#D55E00",      # Naranja quemado
    "Adultos mayores (60+)": "#CC79A7" # Rosa magenta suave
}

fig2, ax2 = plt.subplots(figsize=(5, 5))
etiquetas = ["Primer Voto (17-21)", "Jóvenes (18-25)", "Adultos (26-59)", "Adultos mayores (60+)"]
valores = [total_primervoto, total_jovenes, total_adultos, total_mayores]
colores_pie = list(colors_etarios.values())

wedges, texts, autotexts = ax2.pie(
    valores, labels=None, autopct="%1.1f%%", colors=colores_pie,
    startangle=90, textprops=dict(color="w", fontsize=12, weight='bold')
)
ax2.axis("equal")
ax2.set_title("", fontsize=16, weight='bold')

for autotext in autotexts:
    autotext.set_color('black')

# Leyenda con flechas (anotaciones)
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    ax2.annotate(
        etiquetas[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
        horizontalalignment=horizontalalignment, fontsize=11, weight='bold',
        arrowprops=dict(arrowstyle="-|>", connectionstyle=connectionstyle, color=colores_pie[i])
    )

st.pyplot(fig2)

# 2) Porcentaje Varones y Mujeres por Anexo (100% apilado)
st.subheader("👥 Porcentaje de Varones y Mujeres por Anexo")

fig3, ax3 = plt.subplots(figsize=(12, 7))

anexos = df["Anexo"]
varones = df["% Varones"]
mujeres = df["% Mujeres"]

ax3.barh(anexos, varones, color="#1f77b4", label="Varones")
ax3.barh(anexos, mujeres, left=varones, color="#ff7f0e", label="Mujeres")

for i, (v, m) in enumerate(zip(varones, mujeres)):
    ax3.text(v / 2, i, f"{v:.1f}%", va='center', ha='center', color='white', fontweight='bold')
    ax3.text(v + m / 2, i, f"{m:.1f}%", va='center', ha='center', color='white', fontweight='bold')

ax3.set_xlabel("Porcentaje")
ax3.set_ylabel("Anexo")
ax3.set_title("Distribución Porcentual de Género por Anexo")
ax3.legend(loc='lower right')
ax3.set_xlim(0, 100)
ax3.invert_yaxis()
ax3.grid(axis='x', linestyle='--', alpha=0.7)

st.pyplot(fig3)

# 3) Distribución por segmento etario y anexo (apilado números absolutos)
st.subheader("📊 Distribución por grupos de edad")

fig, ax = plt.subplots(figsize=(12, 7))
bottom = np.zeros(len(df))

for grupo in ["Primer Voto", "Jóvenes (18-25)", "Adultos (26-59)", "Adultos mayores (60+)"]:
    ax.barh(df["Anexo"], df[grupo], left=bottom, color=colors_etarios[grupo], label=grupo)
    for i, val in enumerate(df[grupo]):
        if val > 0:
            ax.text(bottom[i] + val / 2, i, f"{int(val):,}", va="center", ha="center", fontsize=9, color="white", fontweight="bold")
    bottom += df[grupo]

ax.set_xlabel("Número de Votantes")
ax.set_ylabel("Anexo")
ax.set_title("Distribución por Segmento de edades")
ax.invert_yaxis()
ax.legend(loc='lower right')
ax.grid(axis='x', linestyle='--', alpha=0.7)

st.pyplot(fig)

# --- Footer ---
st.markdown("""
    <hr style="margin-top:50px; margin-bottom:20px;">
    <p style="font-size:12px; color:#95a5a6; text-align:center;">
    © 2025 Campaña Política Digital Salas - Todos los derechos reservados - Ricardo Carlos García Hernández
    </p>
""", unsafe_allow_html=True)
