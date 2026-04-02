import streamlit as st


def render_client_example_card() -> None:
	st.markdown("**Ficha de ejemplo**")
	ficha1, ficha2, ficha3 = st.columns(3)

	ficha1.markdown(
		"""
		<div class="card">
			<strong>Cliente</strong><br>
			Ana Lopez<br>
			CL001
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha2.markdown(
		"""
		<div class="card">
			<strong>Contacto</strong><br>
			ana@email.com<br>
			300 123 4567
		</div>
		""",
		unsafe_allow_html=True,
	)

	ficha3.markdown(
		"""
		<div class="card">
			<strong>Estado</strong><br>
			Activo<br>
			VIP
		</div>
		""",
		unsafe_allow_html=True,
	)
