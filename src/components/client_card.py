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

	ficha1.markdown(
		f"""
		<div class="card">
			<strong>Cliente</strong><br>
			{name}<br>
			{client_id}
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha2.markdown(
		f"""
		<div class="card">
			<strong>Contacto</strong><br>
			{email}<br>
			{phone}
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha3.markdown(
		f"""
		<div class="card">
			<strong>Estado</strong><br>
			{status}<br>
			{client_type}
		</div>
		""",
		unsafe_allow_html=True,
	)
