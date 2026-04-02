import streamlit as st


def render_metrics() -> None:
	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Clientes", "128")
	col2.metric("Activos", "97")
	col3.metric("Pendientes", "18")
	col4.metric("Eliminados", "13")
