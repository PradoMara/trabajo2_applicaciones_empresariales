import streamlit as st
from components.client_form import render_delete_permanent_section


def render_delete_view() -> None:
	st.subheader("Eliminar cliente")
	st.warning("Cuidado: Esta sección permite eliminar registros definitivamente de la base de datos.")
	render_delete_permanent_section()
