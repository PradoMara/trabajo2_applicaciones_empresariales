import streamlit as st

from data.db import (
	create_client,
	delete_client,
	get_client_by_id,
	get_next_client_id,
	list_client_options,
	update_client,
)


def _render_flash_message(key: str) -> None:
	message = st.session_state.pop(key, None)
	if not message:
		return

	st.success(message)


def render_register_form() -> None:
	if st.session_state.pop("reset_register_form", False):
		for key in [
			"register_name",
			"register_email",
			"register_phone",
			"register_notes",
			"register_type",
			"register_status",
		]:
			st.session_state.pop(key, None)

	_render_flash_message("register_success")
	next_id = get_next_client_id()
	c1, c2 = st.columns(2)
	with c1:
		st.text_input("Nombre completo", key="register_name")
		st.text_input("Correo electronico", key="register_email")
		st.text_input("Telefono", key="register_phone")

	with c2:
		st.info(f"ID asignado automaticamente: {next_id}")
		st.selectbox("Tipo de cliente", ["Nuevo", "Recurrente", "VIP"], key="register_type")
		st.selectbox(
			"Estado del cliente",
			["Activo", "Pendiente", "Inactivo"],
			key="register_status",
		)

	st.text_area("Observaciones", placeholder="Notas internas sobre el cliente", key="register_notes")
	if st.button("Registrar cliente", type="primary", key="register_submit"):
		success, message, _ = create_client(
			st.session_state.get("register_name", ""),
			st.session_state.get("register_email", ""),
			st.session_state.get("register_phone", ""),
			st.session_state.get("register_type", "Nuevo"),
			st.session_state.get("register_status", "Pendiente"),
			st.session_state.get("register_notes", ""),
		)

		if success:
			st.session_state["reset_register_form"] = True
			st.session_state["register_success"] = message
			st.rerun()
		else:
			st.error(message)


def render_update_form() -> None:
	_render_flash_message("update_success")
	options = list_client_options()
	if not options:
		st.info("No hay clientes disponibles para actualizar.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}

	c1, c2 = st.columns(2)
	with c1:
		selected_label = st.selectbox("Seleccionar cliente", labels, key="update_client")
		selected_id = label_to_id[selected_label]
		selected_client = get_client_by_id(selected_id)

		if selected_client is None:
			st.error("No se pudo cargar la informacion del cliente.")
			return

		st.text_input("Nuevo nombre", key="update_name")
		st.text_input("Nuevo correo", key="update_email")
		st.caption(f"Nombre actual: {selected_client['name']}")
		st.caption(f"Correo actual: {selected_client['email']}")

	with c2:
		st.text_input("Nuevo telefono", key="update_phone")
		st.selectbox("Nuevo tipo", ["Nuevo", "Recurrente", "VIP"], key="update_type")
		st.selectbox("Nuevo estado", ["Activo", "Pendiente", "Inactivo"], key="update_status")
		st.caption(f"Telefono actual: {selected_client['phone'] or 'Sin telefono'}")
		st.caption(f"Tipo actual: {selected_client['client_type']}")
		st.caption(f"Estado actual: {selected_client['status']}")

	st.text_area("Motivo de actualizacion", placeholder="Explica el cambio a realizar", key="update_reason")
	if st.button("Actualizar cliente", type="primary", key="update_submit"):
		success, message = update_client(
			selected_id,
			st.session_state.get("update_name", ""),
			st.session_state.get("update_email", ""),
			st.session_state.get("update_phone", ""),
			st.session_state.get("update_type", selected_client["client_type"]),
			st.session_state.get("update_status", selected_client["status"]),
			st.session_state.get("update_reason", ""),
		)

		if success:
			st.session_state["update_success"] = message
			st.rerun()
		else:
			st.error(message)


def render_delete_section() -> None:
	_render_flash_message("delete_success")
	options = list_client_options()
	if not options:
		st.info("No hay clientes disponibles para eliminar.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}
	selected_label = st.selectbox("Seleccionar cliente para eliminar", labels, key="delete_client")
	selected_id = label_to_id[selected_label]

	st.warning("Esta accion marcara al cliente como Inactivo y dejara de mostrarse en el listado.")
	confirmed = st.checkbox("Confirmo que deseo eliminar este cliente", key="delete_confirm")
	if st.button("Eliminar cliente", type="primary", disabled=not confirmed, key="delete_submit"):
		if delete_client(selected_id):
			st.session_state["delete_success"] = "Cliente desactivado correctamente."
			st.rerun()
		else:
			st.error("No se pudo eliminar el cliente seleccionado.")
