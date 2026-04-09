import streamlit as st

from components.client_card import render_client_card
from data.db import search_clients


def render_get_view() -> None:
	st.subheader("Obtener cliente")
	c1, c2 = st.columns([2, 1])

	with c1:
		query = st.text_input(
			"Buscar por ID, nombre o correo",
			placeholder="Ej. 1 o ana@email.com",
			key="get_query",
		)
		search_clicked = st.button("Buscar", type="primary", key="get_search")

	with c2:
		st.info("Busca un cliente real para ver su ficha.")

	if not search_clicked:
		return

	results = search_clients(query)
	if not results:
		st.warning("No se encontraron clientes con ese criterio.")
		return

	if len(results) == 1:
		render_client_card(results[0])
		return

	st.caption(f"Se encontraron {len(results)} clientes. Selecciona uno:")
	labels = [f"{item['name']} - {item['id']}" for item in results]
	selected_label = st.selectbox("Resultados", labels, key="get_result")
	selected_client = next(item for item in results if f"{item['name']} - {item['id']}" == selected_label)
	render_client_card(selected_client)
