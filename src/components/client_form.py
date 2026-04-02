import streamlit as st


CLIENT_OPTIONS = ["Ana Lopez - CL001", "Carlos Perez - CL002", "Maria Ruiz - CL003"]


def render_register_form() -> None:
	c1, c2 = st.columns(2)
	with c1:
		st.text_input("Nombre completo", key="register_name")
		st.text_input("Correo electronico", key="register_email")
		st.text_input("Telefono", key="register_phone")

	with c2:
		st.text_input("ID cliente", key="register_id")
		st.selectbox("Tipo de cliente", ["Nuevo", "Recurrente", "VIP"], key="register_type")
		st.selectbox(
			"Estado del cliente",
			["Activo", "Pendiente", "Inactivo"],
			key="register_status",
		)

	st.text_area("Observaciones", placeholder="Notas internas sobre el cliente", key="register_notes")
	st.button("Registrar cliente", type="primary", key="register_submit")


def render_update_form() -> None:
	c1, c2 = st.columns(2)
	with c1:
		st.selectbox("Seleccionar cliente", CLIENT_OPTIONS, key="update_client")
		st.text_input("Nuevo nombre", key="update_name")
		st.text_input("Nuevo correo", key="update_email")

	with c2:
		st.text_input("Nuevo telefono", key="update_phone")
		st.selectbox("Nuevo tipo", ["Nuevo", "Recurrente", "VIP"], key="update_type")
		st.selectbox("Nuevo estado", ["Activo", "Pendiente", "Inactivo"], key="update_status")

	st.text_area("Motivo de actualizacion", placeholder="Explica el cambio a realizar", key="update_reason")
	st.button("Actualizar cliente", type="primary", key="update_submit")


def render_delete_section() -> None:
	st.selectbox("Seleccionar cliente para eliminar", CLIENT_OPTIONS, key="delete_client")
	st.warning("Esta seccion es solo visual. La eliminacion real la haras despues.")
	confirmed = st.checkbox("Confirmo que deseo eliminar este cliente", key="delete_confirm")
	st.button("Eliminar cliente", type="primary", disabled=not confirmed, key="delete_submit")
