import streamlit as st

from components.client_card import render_client_example_card


def render_get_view() -> None:
	st.subheader("Obtener cliente")
	c1, c2 = st.columns([2, 1])

	with c1:
		st.text_input(
			"Buscar por ID, nombre o correo",
			placeholder="Ej. CL001 o ana@email.com",
			key="get_query",
		)
		st.button("Buscar", type="primary", key="get_search")

	with c2:
		st.info("Aqui se mostrara la ficha del cliente seleccionado.")

	render_client_example_card()
