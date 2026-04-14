import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "clientes.db"


def get_connection() -> sqlite3.Connection:
	"""Create a SQLite connection for app data access."""
	connection = sqlite3.connect(DB_PATH)
	connection.row_factory = sqlite3.Row
	return connection


def init_db() -> None:
	"""Create required tables if they do not exist yet."""
	with get_connection() as connection:
		# Ensure the clients table uses an autoincrement integer primary key.
		clients_table_exists = connection.execute(
			"""
			SELECT 1
			FROM sqlite_master
			WHERE type = 'table' AND name = 'clients'
			"""
		).fetchone()

		if clients_table_exists:
			id_column = connection.execute("PRAGMA table_info(clients)").fetchall()
			id_info = next((row for row in id_column if row["name"] == "id"), None)
			uses_autoincrement_id = (
				id_info is not None
				and id_info["type"].upper() == "INTEGER"
				and id_info["pk"] == 1
			)

			if not uses_autoincrement_id:
				connection.execute(
					"""
					CREATE TABLE clients_new (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						name TEXT NOT NULL,
						email TEXT UNIQUE NOT NULL,
						phone TEXT,
						client_type TEXT NOT NULL,
						status TEXT NOT NULL,
						notes TEXT,
						created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
						updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
					)
					"""
				)

				connection.execute(
					"""
					INSERT INTO clients_new (id, name, email, phone, client_type, status, notes, created_at, updated_at)
					SELECT
						CASE
							WHEN id GLOB '[0-9]*' THEN CAST(id AS INTEGER)
							ELSE NULL
						END,
						name,
						email,
						phone,
						client_type,
						status,
						notes,
						created_at,
						updated_at
					FROM clients
					"""
				)

				connection.execute("DROP TABLE clients")
				connection.execute("ALTER TABLE clients_new RENAME TO clients")

		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS clients (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				email TEXT UNIQUE NOT NULL,
				phone TEXT,
				client_type TEXT NOT NULL,
				status TEXT NOT NULL,
				notes TEXT,
				created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
				updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)
		connection.commit()


def get_clients() -> list[dict[str, str]]:
	with get_connection() as connection:
		rows = connection.execute(
			"""
			SELECT
				id,
				name,
				status,
				client_type,
				updated_at
			FROM clients
			WHERE status != 'Inactivo'
			ORDER BY updated_at DESC
			"""
		).fetchall()

	return [
		{
			"ID": row["id"],
			"Nombre": row["name"],
			"Estado": row["status"],
			"Tipo": row["client_type"],
			"Ultima actualizacion": row["updated_at"],
		}
		for row in rows
	]


def get_metrics() -> dict[str, int]:
	with get_connection() as connection:
		total = connection.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
		active = connection.execute(
			"SELECT COUNT(*) FROM clients WHERE status = ?", ("Activo",)
		).fetchone()[0]
		pending = connection.execute(
			"SELECT COUNT(*) FROM clients WHERE status = ?", ("Pendiente",)
		).fetchone()[0]
		inactive = connection.execute(
			"SELECT COUNT(*) FROM clients WHERE status = ?", ("Inactivo",)
		).fetchone()[0]

	return {
		"Clientes": total,
		"Activos": active,
		"Pendientes": pending,
		"Inactivos": inactive,
	}


def list_client_options() -> list[dict[str, str]]:
	with get_connection() as connection:
		rows = connection.execute(
			"""
			SELECT id, name
			FROM clients
			WHERE status != 'Inactivo'
			ORDER BY updated_at DESC
			"""
		).fetchall()

	return [{"id": str(row["id"]), "label": f"{row['name']} - {row['id']}"} for row in rows]


def get_client_by_id(client_id: str) -> dict[str, str] | None:
	with get_connection() as connection:
		row = connection.execute(
			"""
			SELECT id, name, email, phone, client_type, status, notes, created_at, updated_at
			FROM clients
			WHERE id = ?
			""",
			(client_id,),
		).fetchone()

	if row is None:
		return None

	return {
		"id": row["id"],
		"name": row["name"],
		"email": row["email"],
		"phone": row["phone"] or "",
		"client_type": row["client_type"],
		"status": row["status"],
		"notes": row["notes"] or "",
		"created_at": row["created_at"],
		"updated_at": row["updated_at"],
	}


def search_clients(query: str) -> list[dict[str, str]]:
	text = query.strip()
	if not text:
		return []

	like_query = f"%{text}%"
	with get_connection() as connection:
		rows = connection.execute(
			"""
			SELECT id, name, email, phone, client_type, status, notes, created_at, updated_at
			FROM clients
			WHERE (id LIKE ? OR name LIKE ? OR email LIKE ?)
				AND status != 'Inactivo'
			ORDER BY updated_at DESC
			LIMIT 20
			""",
			(like_query, like_query, like_query),
		).fetchall()

	return [
		{
			"id": str(row["id"]),
			"name": row["name"],
			"email": row["email"],
			"phone": row["phone"] or "",
			"client_type": row["client_type"],
			"status": row["status"],
			"notes": row["notes"] or "",
			"created_at": row["created_at"],
			"updated_at": row["updated_at"],
		}
		for row in rows
	]


def create_client(
	name: str,
	email: str,
	phone: str,
	client_type: str,
	status: str,
	notes: str,
) -> tuple[bool, str, int | None]:
	clean_name = name.strip()
	clean_email = email.strip()

	if not clean_name or not clean_email:
		return False, "Nombre y correo son obligatorios.", None

	try:
		with get_connection() as connection:
			cursor = connection.execute(
				"""
				INSERT INTO clients (name, email, phone, client_type, status, notes)
				VALUES (?, ?, ?, ?, ?, ?)
				""",
				(
					clean_name,
					clean_email,
					phone.strip(),
					client_type,
					status,
					notes.strip(),
				),
			)
			new_id = cursor.lastrowid
			connection.commit()
	except sqlite3.IntegrityError:
		return False, "No se pudo registrar: el correo ya existe.", None

	return True, f"Cliente registrado correctamente con ID {new_id}.", new_id


def update_client(
	client_id: str,
	name: str,
	email: str,
	phone: str,
	client_type: str,
	status: str,
	notes: str,
) -> tuple[bool, str]:
	current_client = get_client_by_id(client_id)
	if current_client is None:
		return False, "El cliente seleccionado no existe."

	new_name = name.strip() or current_client["name"]
	new_email = email.strip() or current_client["email"]
	new_phone = phone.strip() if phone.strip() else current_client["phone"]
	new_notes = notes.strip() if notes.strip() else current_client["notes"]

	try:
		with get_connection() as connection:
			connection.execute(
				"""
				UPDATE clients
				SET
					name = ?,
					email = ?,
					phone = ?,
					client_type = ?,
					status = ?,
					notes = ?,
					updated_at = CURRENT_TIMESTAMP
				WHERE id = ?
				""",
				(new_name, new_email, new_phone, client_type, status, new_notes, client_id),
			)
			connection.commit()
	except sqlite3.IntegrityError:
		return False, "No se pudo actualizar: el correo ya esta en uso."

	return True, "Cliente actualizado correctamente."


def delete_client(client_id: str) -> bool:
	with get_connection() as connection:
		cursor = connection.execute(
			"""
			UPDATE clients
			SET status = 'Inactivo', updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
			""",
			(client_id,),
		)
		connection.commit()

	return cursor.rowcount > 0

