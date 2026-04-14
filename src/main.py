import streamlit as st

from app.header import render_header
from app.layout import configure_page, render_footer
from app.sidebar import render_sidebar
from components.metrics import render_metrics
from data.db import init_db
from styles.theme import apply_theme
from views.delete_view import render_delete_view
from views.get_view import render_get_view
from views.list_view import render_list_view
from views.register_view import render_register_view
from views.update_view import render_update_view


def main() -> None:
    init_db()
    configure_page()
    apply_theme()

    render_header()
    render_metrics()
    filters = render_sidebar()

    tab_registrar, tab_actualizar, tab_obtener, tab_eliminar, tab_listado = st.tabs(
        ["Registrar", "Actualizar", "Obtener", "Eliminar", "Ver clientes"]
    )

    with tab_registrar:
        render_register_view()

    with tab_actualizar:
        render_update_view()

    with tab_obtener:
        render_get_view()

    with tab_eliminar:
        render_delete_view()

    with tab_listado:
        render_list_view(filters)

    render_footer()


if __name__ == "__main__":
    main()