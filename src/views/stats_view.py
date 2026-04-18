import streamlit as st
from components.metrics import render_metrics

def render_stats_view() -> None:
    st.subheader("📊 Estadísticas y Análisis de Datos")
    st.write("Visualización global del estado de los clientes y distribución de la cartera.")
    render_metrics()
