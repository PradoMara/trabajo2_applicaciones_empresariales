import streamlit as st

from data.db import get_clients


def render_clients_table() -> None:
	st.subheader("Listado de clientes")
	clients = get_clients()
	if not clients:
		st.info("No hay clientes registrados en la base de datos.")
		return

	st.dataframe(clients, use_container_width=True, hide_index=True)
