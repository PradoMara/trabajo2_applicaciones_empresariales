import streamlit as st

from app.header import render_header
from app.layout import configure_page, render_footer
from app.sidebar import render_sidebar
from components.client_table import render_clients_table
from components.metrics import render_metrics
from data.db import init_db
from styles.theme import apply_theme
from views.delete_view import render_delete_view
from views.get_view import render_get_view
from views.register_view import render_register_view
from views.update_view import render_update_view


def main() -> None:
    init_db()
    configure_page()
    apply_theme()

    render_header()
    render_metrics()
    render_sidebar()

    tab_registrar, tab_actualizar, tab_obtener, tab_eliminar = st.tabs(
        ["Registrar", "Actualizar", "Obtener", "Eliminar"]
    )

    with tab_registrar:
        render_register_view()

    with tab_actualizar:
        render_update_view()

    with tab_obtener:
        render_get_view()

    with tab_eliminar:
        render_delete_view()

    st.divider()
    render_clients_table()
    render_footer()


if __name__ == "__main__":
    main()