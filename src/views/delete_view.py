import streamlit as st

from components.client_form import render_delete_section


def render_delete_view() -> None:
	st.subheader("Eliminar cliente")
	render_delete_section()
