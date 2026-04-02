import streamlit as st


MOCK_CLIENTS = [
	{
		"ID": "CL001",
		"Nombre": "Ana Lopez",
		"Estado": "Activo",
		"Tipo": "VIP",
		"Ultima actualizacion": "2026-04-02",
	},
	{
		"ID": "CL002",
		"Nombre": "Carlos Perez",
		"Estado": "Pendiente",
		"Tipo": "Nuevo",
		"Ultima actualizacion": "2026-04-01",
	},
	{
		"ID": "CL003",
		"Nombre": "Maria Ruiz",
		"Estado": "Inactivo",
		"Tipo": "Recurrente",
		"Ultima actualizacion": "2026-03-30",
	},
]


def render_clients_table() -> None:
	st.subheader("Listado de clientes")
	st.dataframe(MOCK_CLIENTS, use_container_width=True, hide_index=True)
