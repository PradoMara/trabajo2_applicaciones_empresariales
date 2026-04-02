from datetime import datetime

import streamlit as st


def configure_page() -> None:
	st.set_page_config(page_title="Registro de Clientes", page_icon="👥", layout="wide")


def render_footer() -> None:
	st.caption(f"Vista generada el {datetime.now().strftime('%Y-%m-%d %H:%M')}")
