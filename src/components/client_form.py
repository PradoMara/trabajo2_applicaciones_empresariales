import re
import streamlit as st

from data.db import (
	CLIENT_TYPE_OPTIONS,
	create_client,
	deactivate_client,
	get_client_audit_log,
	get_client_by_id,
	list_all_client_options,
	list_inactive_client_options,
	list_client_options,
	reactivate_client,
	update_client,
)


def _render_flash_message(key: str) -> None:
	message = st.session_state.pop(key, None)
	if message:
		st.success(message)


def _is_valid_email(email: str) -> bool:
	"""
	Valida el formato de un correo electrónico usando expresiones regulares
	para permitir cualquier dominio válido.
	"""
	value = email.strip()
	if not value:
		return False
	
	# Expresión regular para validar correos electrónicos estándar
	pattern = r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
	return bool(re.match(pattern, value))


def _is_valid_phone(phone: str) -> bool:
	value = phone.replace(" ", "").strip()
	if not value:
		return True

	return (
		len(value) > 8
		and (value.isdigit() or (value.startswith("+") and value[1:].isdigit()))
	)


def _is_valid_name(name: str, allow_digits: bool) -> bool:
	"""
	Valida que el nombre tenga una longitud adecuada (3-30 caracteres),
	contenga al menos una letra y respete la restricción de dígitos.
	"""
	value = name.strip()
	
	#Validacion Longitud nombre
	if len(value) < 3 or len(value) > 30:
		return False

	# Debe contener al menos una letra
	has_letter = any(char.isalpha() for char in value)
	if not has_letter:
		return False

	# Si no se permiten dígitos (persona natural), no debe tener números
	if not allow_digits and any(char.isdigit() for char in value):
		return False
	
	# No permitir caracteres especiales problemáticos (permitir espacios, puntos, tildes y ñ)
	# Solo permite letras, números (si allow_digits es True), espacios y signos básicos de puntuación
	if allow_digits:
		pattern = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.]+$'
	else:
		pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.]+$'
		
	return bool(re.match(pattern, value))


def render_register_form() -> None:
	if st.session_state.pop("reset_register_form", False):
		for key in [
			"register_name",
			"register_allow_digits_name",
			"register_email",
			"register_phone",
			"register_notes",
			"register_type",
			"register_status",
		]:
			st.session_state.pop(key, None)

	_render_flash_message("register_success")
	c1, c2 = st.columns(2)

	with c1:
		st.text_input("Nombre completo", key="register_name")
		allow_digits_name = st.checkbox(
			"Es empresa o razon social (permitir numeros en el nombre)",
			key="register_allow_digits_name",
		)
		name = st.session_state.get("register_name", "")
		name_is_valid = _is_valid_name(name, allow_digits_name)
		if name:
			if not name_is_valid:
				if len(name.strip()) < 3:
					st.error("El nombre debe tener al menos 3 caracteres.")
				elif len(name.strip()) > 30:
					st.error("El nombre no puede exceder los 30 caracteres.")
				elif not any(char.isalpha() for char in name):
					st.error("El nombre debe contener al menos una letra.")
				elif not allow_digits_name and any(char.isdigit() for char in name):
					st.error("El nombre no puede incluir números salvo que marques que es empresa.")
				else:
					st.error("El nombre solo puede contener letras, números (si es empresa), espacios y puntos.")
		
		email = st.text_input("Correo electronico", key="register_email")
		if email and not _is_valid_email(email):
			st.error("El formato del correo no es válido.")

		phone = st.text_input("Telefono", key="register_phone")
		if phone:
			phone_cleaned = phone.replace(" ", "")
			is_number = phone_cleaned.isdigit() or (
				phone_cleaned.startswith("+") and phone_cleaned[1:].isdigit()
			)
			if not is_number:
				st.error("El telefono debe contener unicamente numeros (o empezar con '+').")
			elif len(phone_cleaned) <= 8:
				st.warning("El telefono debe tener mas de 8 digitos.")

	with c2:
		st.info("El ID se asigna automaticamente al registrar.")
		st.selectbox("Tipo de cliente", list(CLIENT_TYPE_OPTIONS), key="register_type")
		st.selectbox(
			"Estado del cliente",
			["Activo", "Pendiente"],
			key="register_status",
		)

	st.text_area(
		"Observaciones",
		placeholder="Notas internas sobre el cliente",
		key="register_notes",
		max_chars=300,
	)

	if st.button("Registrar cliente", type="primary", key="register_submit"):
		name = st.session_state.get("register_name", "")
		allow_digits_name = st.session_state.get("register_allow_digits_name", False)
		email = st.session_state.get("register_email", "")
		phone = st.session_state.get("register_phone", "")

		if (
			not _is_valid_name(name, allow_digits_name)
			or not _is_valid_email(email)
			or not _is_valid_phone(phone)
		):
			st.error("Error al registrar: Revisa los campos requeridos y su formato.")
			return

		success, message, _ = create_client(
			name,
			email,
			phone,
			st.session_state.get("register_type", CLIENT_TYPE_OPTIONS[0]),
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

	selected_label = st.selectbox("Seleccionar cliente", labels, key="update_client")
	selected_id = label_to_id[selected_label]
	selected_client = get_client_by_id(selected_id)
	if selected_client is None:
		st.error("No se pudo cargar la informacion del cliente.")
		return

	if st.session_state.get("update_loaded_id") != selected_id:
		st.session_state["update_loaded_id"] = selected_id
		st.session_state["update_name"] = selected_client["name"]
		st.session_state["update_allow_digits_name"] = any(
			char.isdigit() for char in selected_client["name"]
		)
		st.session_state["update_email"] = selected_client["email"]
		st.session_state["update_phone"] = selected_client["phone"]
		st.session_state["update_type"] = selected_client["client_type"]
		st.session_state["update_status"] = selected_client["status"]
		st.session_state["update_reason"] = selected_client["notes"]

	c1, c2 = st.columns(2)
	with c1:
		st.text_input("Nuevo nombre", key="update_name")
		allow_digits_name = st.checkbox(
			"Es empresa o razon social (permitir numeros en el nombre)",
			key="update_allow_digits_name",
		)
		name = st.session_state.get("update_name", "")
		name_is_valid = _is_valid_name(name, allow_digits_name)
		if name:
			if not name_is_valid:
				if len(name.strip()) < 3:
					st.error("El nombre debe tener al menos 3 caracteres.")
				elif len(name.strip()) > 100:
					st.error("El nombre no puede exceder los 100 caracteres.")
				elif not any(char.isalpha() for char in name):
					st.error("El nombre debe contener al menos una letra.")
				elif not allow_digits_name and any(char.isdigit() for char in name):
					st.error("El nombre no puede incluir números salvo que marques que es empresa.")
				else:
					st.error("El nombre solo puede contener letras, números (si es empresa), espacios y puntos.")
		
		email = st.text_input("Nuevo correo", key="update_email")
		if email and not _is_valid_email(email):
			st.error("El formato del correo no es válido.")

	with c2:
		phone = st.text_input("Nuevo telefono", key="update_phone")
		if phone:
			phone_cleaned = phone.replace(" ", "")
			is_number = phone_cleaned.isdigit() or (
				phone_cleaned.startswith("+") and phone_cleaned[1:].isdigit()
			)
			if not is_number:
				st.error("El telefono debe contener unicamente numeros (o empezar con '+').")
			elif len(phone_cleaned) <= 8:
				st.warning("El telefono debe tener mas de 8 digitos.")
		st.selectbox("Nuevo tipo", list(CLIENT_TYPE_OPTIONS), key="update_type")
		st.selectbox("Nuevo estado", ["Activo", "Pendiente", "Inactivo"], key="update_status")

	st.text_area(
		"Observaciones del cliente",
		placeholder="Notas internas sobre el cliente",
		key="update_reason",
		max_chars=800,
	)
	st.text_area(
		"Motivo del cambio (auditoria)",
		placeholder="Describe por que se realiza esta modificacion",
		key="update_audit_reason",
		max_chars=300,
	)

	if st.button("Actualizar cliente", type="primary", key="update_submit"):
		new_name = st.session_state.get("update_name", "")
		allow_digits_name = st.session_state.get("update_allow_digits_name", False)
		new_email = st.session_state.get("update_email", "")
		new_phone = st.session_state.get("update_phone", "")
		new_type = st.session_state.get("update_type", selected_client["client_type"])
		new_status = st.session_state.get("update_status", selected_client["status"])
		new_notes = st.session_state.get("update_reason", selected_client["notes"])
		audit_reason = st.session_state.get("update_audit_reason", "")

		if (
			not _is_valid_name(new_name, allow_digits_name)
			or not _is_valid_email(new_email)
			or not _is_valid_phone(new_phone)
		):
			st.error("Error al actualizar: Revisa los campos requeridos y su formato.")
			return

		has_changes = any(
			[
				new_name.strip() != selected_client["name"],
				new_email.strip() != selected_client["email"],
				new_phone.strip() != selected_client["phone"],
				new_type != selected_client["client_type"],
				new_status != selected_client["status"],
				new_notes.strip() != selected_client["notes"],
			]
		)
		if not has_changes:
			st.warning("No se han detectado cambios. Los datos ingresados son identicos a los actuales.")
			return

		success, message = update_client(
			selected_id,
			new_name,
			new_email,
			new_phone,
			new_type,
			new_status,
			new_notes,
			audit_reason,
		)
		if success:
			st.session_state["update_success"] = message
			st.rerun()
		else:
			st.error(message)


def render_deactivate_section() -> None:
	_render_flash_message("deactivate_success")
	options = list_client_options()
	if not options:
		st.info("No hay clientes disponibles para desactivar.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}
	selected_label = st.selectbox("Seleccionar cliente para desactivar", labels, key="deactivate_client")
	selected_id = label_to_id[selected_label]

	st.warning("Esta accion marcara al cliente como Inactivo y dejara de mostrarse en el listado.")
	confirmed = st.checkbox("Confirmo que deseo desactivar este cliente", key="deactivate_confirm")
	if st.button("Desactivar cliente", type="primary", disabled=not confirmed, key="deactivate_submit"):
		if deactivate_client(selected_id):
			st.session_state["deactivate_success"] = "Cliente desactivado correctamente."
			st.rerun()
		else:
			st.error("No se pudo desactivar el cliente seleccionado.")


def render_reactivate_section() -> None:
	_render_flash_message("reactivate_success")
	options = list_inactive_client_options()
	if not options:
		st.info("No hay clientes inactivos para reactivar.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}
	selected_label = st.selectbox("Seleccionar cliente para reactivar", labels, key="reactivate_client")
	selected_id = label_to_id[selected_label]

	st.info("Esta accion cambiara el estado del cliente a Activo.")
	confirmed = st.checkbox("Confirmo que deseo reactivar este cliente", key="reactivate_confirm")
	if st.button("Reactivar cliente", type="primary", disabled=not confirmed, key="reactivate_submit"):
		if reactivate_client(selected_id):
			st.session_state["reactivate_success"] = "Cliente reactivado correctamente."
			st.rerun()
		else:
			st.error("No se pudo reactivar el cliente seleccionado.")


def render_audit_log_section() -> None:
	options = list_all_client_options()
	if not options:
		st.info("No hay clientes registrados para consultar historial.")
		return

	labels = [item["label"] for item in options]
	label_to_id = {item["label"]: item["id"] for item in options}
	selected_label = st.selectbox("Seleccionar cliente", labels, key="audit_client")
	selected_id = label_to_id[selected_label]

	logs = get_client_audit_log(selected_id)
	if not logs:
		st.info("Este cliente aun no tiene cambios auditados.")
		return

	st.dataframe(logs, use_container_width=True, hide_index=True)
