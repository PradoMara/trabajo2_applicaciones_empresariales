import streamlit as st
from data.db import get_clients


def render_clients_table(filters: dict[str, str]) -> None:
	st.subheader("Listado de clientes")
	clients = get_clients(
		estado=filters.get("estado", "Todos"),
		segmento=filters.get("segmento", "Todos"),
		busqueda=filters.get("busqueda", ""),
	)
	if not clients:
		st.info("No hay clientes que coincidan con los filtros seleccionados.")
		return

	st.dataframe(clients, use_container_width=True, hide_index=True)
