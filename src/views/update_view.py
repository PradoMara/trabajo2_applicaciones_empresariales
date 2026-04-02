import streamlit as st

from components.client_form import render_update_form


def render_update_view() -> None:
	st.subheader("Actualizar cliente")
	render_update_form()
