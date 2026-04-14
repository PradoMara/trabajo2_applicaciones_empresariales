import html

import streamlit as st


def render_client_card(client: dict[str, str]) -> None:
	st.markdown("**Ficha del cliente**")
	ficha1, ficha2, ficha3 = st.columns(3)
	name = client["name"]
	client_id = client["id"]
	email = client["email"]
	phone = client["phone"] or "Sin telefono"
	status = client["status"]
	client_type = client["client_type"]

	# Escape user-controlled values before rendering with unsafe HTML.
	name_safe = html.escape(str(name))
	client_id_safe = html.escape(str(client_id))
	email_safe = html.escape(str(email))
	phone_safe = html.escape(str(phone))
	status_safe = html.escape(str(status))
	client_type_safe = html.escape(str(client_type))

	ficha1.markdown(
		f"""
		<div class="card">
			<strong>Cliente</strong><br>
			{name_safe}<br>
			{client_id_safe}
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha2.markdown(
		f"""
		<div class="card">
			<strong>Contacto</strong><br>
			{email_safe}<br>
			{phone_safe}
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha3.markdown(
		f"""
		<div class="card">
			<strong>Estado</strong><br>
			{status_safe}<br>
			{client_type_safe}
		</div>
		""",
		unsafe_allow_html=True,
	)
