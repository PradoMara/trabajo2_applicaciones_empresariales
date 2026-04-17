import streamlit as st

from components.client_form import render_audit_log_section


def render_audit_view() -> None:
	st.subheader("Historial de cambios")
	render_audit_log_section()
