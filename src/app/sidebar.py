import streamlit as st


def render_sidebar() -> dict:
	with st.sidebar:
		st.header("Filtros")
		estado = st.selectbox("Estado", ["Todos", "Activo", "Pendiente", "Inactivo"])
		segmento = st.selectbox("Segmento", ["Todos", "Premium", "PyME", "Corporativo"])
		busqueda = st.text_input("Buscar cliente", placeholder="Nombre, email o ID")

	return {
		"estado": estado,
		"segmento": segmento,
		"busqueda": busqueda,
	}
