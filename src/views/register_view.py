import streamlit as st

from components.client_form import render_register_form


def render_register_view() -> None:
	st.subheader("Registrar cliente")
	render_register_form()
