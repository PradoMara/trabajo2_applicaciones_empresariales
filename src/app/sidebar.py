import streamlit as st
from data.db import CLIENT_TYPE_OPTIONS


def render_sidebar() -> dict:
	with st.sidebar:
		st.header("Filtros")
		estado = st.selectbox(
			"Estado",
			["Todos", "Activo", "Pendiente", "Inactivo"],
			key="filter_estado",
		)
		segmento = st.selectbox(
			"Segmento",
			["Todos", *CLIENT_TYPE_OPTIONS],
			key="filter_segmento",
		)
		busqueda = st.text_input(
			"Buscar cliente",
			placeholder="Nombre, email o ID",
			key="filter_busqueda",
		)

	return {
		"estado": estado,
		"segmento": segmento,
		"busqueda": busqueda,
	}
