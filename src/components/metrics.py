import streamlit as st
from data.db import get_metrics


def render_metrics() -> None:
	metrics = get_metrics()
	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Clientes", str(metrics.get("Clientes", 0)))
	col2.metric("Activos", str(metrics.get("Activos", 0)))
	col3.metric("Pendientes", str(metrics.get("Pendientes", 0)))
	col4.metric("Inactivos", str(metrics.get("Inactivos", 0)))
