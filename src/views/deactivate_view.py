import streamlit as st

from components.client_form import render_deactivate_section


def render_deactivate_view() -> None:
	st.subheader("Desactivar cliente")
	render_deactivate_section()
