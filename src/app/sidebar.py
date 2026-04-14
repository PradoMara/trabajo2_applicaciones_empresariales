import streamlit as st


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
			["Todos", "Nuevo", "Recurrente", "VIP"],
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
