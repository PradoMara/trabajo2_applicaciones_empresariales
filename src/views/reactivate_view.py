import streamlit as st

from components.client_form import render_reactivate_section


def render_reactivate_view() -> None:
	st.subheader("Reactivar cliente")
	render_reactivate_section()
