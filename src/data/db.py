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
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS clients (
				id TEXT PRIMARY KEY,
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

