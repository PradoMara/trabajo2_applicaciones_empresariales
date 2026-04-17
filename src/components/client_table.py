import streamlit as st
import csv
import importlib
from datetime import datetime
from io import BytesIO, StringIO

from data.db import get_clients, count_clients


def _build_csv_bytes(rows: list[dict[str, str]]) -> bytes:
	if not rows:
		return b""

	buffer = StringIO()
	fieldnames = list(rows[0].keys())
	writer = csv.DictWriter(buffer, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(rows)
	return buffer.getvalue().encode("utf-8-sig")


def _build_excel_bytes(rows: list[dict[str, str]]) -> bytes:
	openpyxl_module = importlib.import_module("openpyxl")
	workbook = openpyxl_module.Workbook()
	worksheet = workbook.active
	worksheet.title = "Clientes"

	if rows:
		headers = list(rows[0].keys())
		worksheet.append(headers)
		for row in rows:
			worksheet.append([row.get(header, "") for header in headers])

	output = BytesIO()
	workbook.save(output)
	return output.getvalue()


def render_clients_table(filters: dict[str, str]) -> None:
	st.subheader("Listado de clientes")
	current_date = datetime.now().strftime("%Y%m%d")

	all_filtered_clients = get_clients(
		estado=filters.get("estado", "Todos"),
		segmento=filters.get("segmento", "Todos"),
		busqueda=filters.get("busqueda", ""),
	)
	excel_enabled = importlib.util.find_spec("openpyxl") is not None

	csv_data = _build_csv_bytes(all_filtered_clients)
	excel_data = _build_excel_bytes(all_filtered_clients) if excel_enabled else b""

	export_col_csv, export_col_excel = st.columns(2)
	with export_col_csv:
		st.download_button(
			label="Exportar CSV",
			data=csv_data,
			file_name=f"clientes_{current_date}.csv",
			mime="text/csv",
			disabled=not all_filtered_clients,
		)
	with export_col_excel:
		if not excel_enabled:
			st.caption("Para exportar Excel, instala la dependencia openpyxl.")
		st.download_button(
			label="Exportar Excel",
			data=excel_data,
			file_name=f"clientes_{current_date}.xlsx",
			mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			disabled=(not all_filtered_clients) or (not excel_enabled),
		)
	
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
