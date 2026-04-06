import streamlit as st

from data.db import get_metrics


def render_metrics() -> None:
	metrics = get_metrics()
	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Clientes", str(metrics["Clientes"]))
	col2.metric("Activos", str(metrics["Activos"]))
	col3.metric("Pendientes", str(metrics["Pendientes"]))
	col4.metric("Inactivos", str(metrics["Inactivos"]))
