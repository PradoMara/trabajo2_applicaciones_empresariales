import streamlit as st
from data.db import get_clients, count_clients


def render_clients_table(filters: dict[str, str]) -> None:
	st.subheader("Listado de clientes")
	
	# Parámetros de paginación
	limit = 10
	
	# Obtener el total de clientes para calcular el número de páginas
	total_clients = count_clients(
		estado=filters.get("estado", "Todos"),
		segmento=filters.get("segmento", "Todos"),
		busqueda=filters.get("busqueda", ""),
	)
	
	if total_clients == 0:
		st.info("No hay clientes que coincidan con los filtros seleccionados.")
		return

	total_pages = (total_clients + limit - 1) // limit
	
	# Usar session_state para mantener la página actual
	if "current_page" not in st.session_state:
		st.session_state.current_page = 1
		
	# Reiniciar a la página 1 si los filtros cambian
	filter_str = f"{filters.get('estado')}_{filters.get('segmento')}_{filters.get('busqueda')}"
	if st.session_state.get("last_filter_str") != filter_str:
		st.session_state.current_page = 1
		st.session_state.last_filter_str = filter_str

	# Obtener clientes para la página actual
	offset = (st.session_state.current_page - 1) * limit
	clients = get_clients(
		estado=filters.get("estado", "Todos"),
		segmento=filters.get("segmento", "Todos"),
		busqueda=filters.get("busqueda", ""),
		limit=limit,
		offset=offset,
	)

	# Mostrar tabla
	st.dataframe(clients, use_container_width=True, hide_index=True)
	
	# Controles de paginación
	c1, c2, c3 = st.columns([1, 2, 1])
	with c1:
		if st.button("Anterior", disabled=st.session_state.current_page <= 1):
			st.session_state.current_page -= 1
			st.rerun()
	with c2:
		st.write(f"Página {st.session_state.current_page} de {total_pages} ({total_clients} clientes)")
	with c3:
		if st.button("Siguiente", disabled=st.session_state.current_page >= total_pages):
			st.session_state.current_page += 1
			st.rerun()
