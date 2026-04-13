import streamlit as st
import time

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
		email = st.text_input("Correo electronico", key="register_email")
		if email:
			email_trimmed = email.strip()
			if "@" not in email_trimmed or not (email_trimmed.endswith(".com") or email_trimmed.endswith(".cl")):
				st.error("El correo debe incluir '@' y terminar en '.com' o '.cl'.")
		
		phone = st.text_input("Telefono", key="register_phone")
		if phone:
			# Eliminamos espacios en blanco automáticamente
			phone_cleaned = phone.replace(" ", "")
			
			# Verificamos si contiene solo números o empieza con + seguido de números
			is_valid_format = phone_cleaned.isdigit() or (phone_cleaned.startswith("+") and phone_cleaned[1:].isdigit())
			
			if not is_valid_format:
				st.error("El teléfono debe contener únicamente números (o empezar con '+').")
			elif len(phone_cleaned) <= 8:
				st.warning("El teléfono debe tener más de 8 dígitos.")

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
	st.text_area("Observaciones", placeholder="Notas internas sobre el cliente", key="register_notes", max_chars=800)
	if st.button("Registrar cliente", type="primary", key="register_submit"):
		name = st.session_state.get("register_name")
		email = st.session_state.get("register_email", "")
		phone = st.session_state.get("register_phone", "")
		client_id = st.session_state.get("register_id")

		if success:
			st.session_state["reset_register_form"] = True
			st.session_state["register_success"] = message
			st.rerun()
		else:
			st.error(message)
		# Limpieza de espacios
		email_trimmed = email.strip()
		phone_cleaned = phone.replace(" ", "")


		# Simulación de validación final antes de "éxito"
		if name and email_trimmed and phone_cleaned and client_id and "@" in email_trimmed and (email_trimmed.endswith(".com") or email_trimmed.endswith(".cl")) and (phone_cleaned.isdigit() or (phone_cleaned.startswith("+") and phone_cleaned[1:].isdigit())) and len(phone_cleaned) > 8:
			st.success(f"✅ Cliente **{name}** registrado correctamente")
		else:
			st.error("Error al registrar: Por favor, complete todos los campos correctamente.")


def render_update_form() -> None:
	_render_flash_message("update_success")
	options = list_client_options()
	if not options:
		st.info("No hay clientes disponibles para actualizar.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}

	# Datos actuales simulados de los clientes
	current_data = {
		"Ana Lopez - CL001": {"name": "Ana Lopez", "email": "ana@email.com", "phone": "3001234567", "type": "Nuevo", "status": "Activo"},
		"Carlos Perez - CL002": {"name": "Carlos Perez", "email": "carlos@email.com", "phone": "3007654321", "type": "Recurrente", "status": "Pendiente"},
		"Maria Ruiz - CL003": {"name": "Maria Ruiz", "email": "maria@email.com", "phone": "3000000000", "type": "VIP", "status": "Inactivo"}
	}

	c1, c2 = st.columns(2)
	with c1:
		selected_label = st.selectbox("Seleccionar cliente", labels, key="update_client")
		selected_id = label_to_id[selected_label]
		selected_client = get_client_by_id(selected_id)

		if selected_client is None:
			st.error("No se pudo cargar la informacion del cliente.")
			return

		selected_client = st.selectbox("Seleccionar cliente", CLIENT_OPTIONS, key="update_client")
		st.text_input("Nuevo nombre", key="update_name")
		st.text_input("Nuevo correo", key="update_email")
		st.caption(f"Nombre actual: {selected_client['name']}")
		st.caption(f"Correo actual: {selected_client['email']}")
		email = st.text_input("Nuevo correo", key="update_email")
		if email:
			email_trimmed = email.strip()
			if "@" not in email_trimmed or not (email_trimmed.endswith(".com") or email_trimmed.endswith(".cl")):
				st.error("El correo debe incluir '@' y terminar en '.com' o '.cl'.")

	with c2:
		phone = st.text_input("Nuevo telefono", key="update_phone")
		if phone:
			# Limpieza y validación
			phone_cleaned = phone.replace(" ", "")
			is_valid_format = phone_cleaned.isdigit() or (phone_cleaned.startswith("+") and phone_cleaned[1:].isdigit())
			
			if not is_valid_format:
				st.error("El teléfono debe contener únicamente números (o empezar con '+').")
			elif len(phone_cleaned) <= 8:
				st.warning("El teléfono debe tener más de 8 dígitos.")
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
	st.text_area("Motivo de actualizacion", placeholder="Explica el cambio a realizar", key="update_reason", max_chars=800)
	if st.button("Actualizar cliente", type="primary", key="update_submit"):
		new_name = st.session_state.get("update_name")
		new_email = st.session_state.get("update_email", "")
		new_phone = st.session_state.get("update_phone", "")
		new_type = st.session_state.get("update_type")
		new_status = st.session_state.get("update_status")

		if success:
			st.session_state["update_success"] = message
			st.rerun()
		else:
			st.error(message)
		# Limpieza de espacios
		new_email_trimmed = new_email.strip()
		new_phone_cleaned = new_phone.replace(" ", "")


		# Validaciones básicas
		if selected_client and new_name and new_email_trimmed and new_phone_cleaned and "@" in new_email_trimmed and (new_email_trimmed.endswith(".com") or new_email_trimmed.endswith(".cl")) and (new_phone_cleaned.isdigit() or (new_phone_cleaned.startswith("+") and new_phone_cleaned[1:].isdigit())) and len(new_phone_cleaned) > 8:
			
			# Validación de cambios reales
			current = current_data.get(selected_client)
			if (new_name == current["name"] and 
				new_email_trimmed == current["email"] and 
				new_phone_cleaned == current["phone"] and 
				new_type == current["type"] and 
				new_status == current["status"]):
				st.warning("⚠️ No se han detectado cambios. Los datos ingresados son idénticos a los actuales.")
			else:
				st.success(f"✅ Datos de **{selected_client}** actualizados exitosamente")
		else:
			st.error("Error al actualizar: Asegúrate de completar todos los campos válidos.")


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
	st.selectbox("Seleccionar cliente para eliminar", CLIENT_OPTIONS, key="delete_client")
	st.warning("Esta seccion es visual hasta que se implemente una base de datos.")
	confirmed = st.checkbox("Confirmo que deseo eliminar este cliente", key="delete_confirm")
	if st.button("Eliminar cliente", type="primary", disabled=not confirmed, key="delete_submit"):
		if delete_client(selected_id):
			st.session_state["delete_success"] = "Cliente desactivado correctamente."
			st.rerun()
		else:
			st.error("No se pudo eliminar el cliente seleccionado.")
	if st.button("Eliminar cliente", type="primary", disabled=not confirmed, key="delete_submit"):
		client = st.session_state.get("delete_client")
		if confirmed and client:
			st.success(f"🗑️ El cliente **{client}** ha sido eliminado")
		else:
			st.error("Error al eliminar: No se ha confirmado la eliminación.")
