import streamlit as st
import time

from components.client_card import render_client_example_card


def render_get_view() -> None:
	st.subheader("Obtener cliente")
	c1, c2 = st.columns([2, 1])

	# Lista de clientes válidos (debería coincidir con los de client_form.py en una app real)
	valid_clients = {
		"CL001": {"name": "Ana Lopez", "email": "ana@email.com", "phone": "300 123 4567", "type": "Nuevo", "status": "Activo"},
		"CL002": {"name": "Carlos Perez", "email": "carlos@email.com", "phone": "300 765 4321", "type": "Recurrente", "status": "Pendiente"},
		"CL003": {"name": "Maria Ruiz", "email": "maria@email.com", "phone": "300 000 0000", "type": "VIP", "status": "Inactivo"}
	}

	found_client = None

	with c1:
		query = st.text_input(
			"Buscar por ID exacto (Ej: CL001, CL002, CL003)",
			placeholder="Ingrese ID del cliente",
			key="get_query",
		)
		if st.button("Buscar", type="primary", key="get_search"):
			if query in valid_clients:
				found_client = valid_clients[query]
				st.success(f"✅ Cliente **{found_client['name']}** encontrado")
			elif not query:
				st.error("Por favor, ingrese un ID para buscar.")
			else:
				st.error(f"No se encontró ningún cliente con el ID '{query}'.")

	with c2:
		if found_client:
			st.info(f"Mostrando ficha de: {found_client['name']}")
		else:
			st.info("No hay nadie para mostrar.")

	if found_client:
		# Renderizamos la ficha con datos reales del encontrado
		st.markdown(f"**Ficha de {found_client['name']}**")
		ficha1, ficha2, ficha3 = st.columns(3)

		ficha1.markdown(
			f"""
			<div class="card">
				<strong>Cliente</strong><br>
				{found_client['name']}<br>
				{query}
			</div>
			""",
			unsafe_allow_html=True,
		)

		ficha2.markdown(
			f"""
			<div class="card">
				<strong>Contacto</strong><br>
				{found_client['email']}<br>
				{found_client['phone']}
			</div>
			""",
			unsafe_allow_html=True,
		)

		ficha3.markdown(
			f"""
			<div class="card">
				<strong>Estado</strong><br>
				{found_client['status']}<br>
				{found_client['type']}
			</div>
			""",
			unsafe_allow_html=True,
		)
	else:
		st.write("---")
		st.caption("Realiza una búsqueda válida para ver la información detallada.")
