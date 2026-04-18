import streamlit as st

from app.header import render_header
from app.layout import configure_page, render_footer
from components.metrics import render_metrics
from data.db import init_db
from styles.theme import apply_theme
from views.audit_view import render_audit_view
from views.deactivate_view import render_deactivate_view
from views.delete_view import render_delete_view
from views.get_view import render_get_view
from views.list_view import render_list_view
from views.reactivate_view import render_reactivate_view
from views.register_view import render_register_view
from views.update_view import render_update_view
from views.stats_view import render_stats_view


def main() -> None:
    init_db()
    configure_page()
    apply_theme()

    render_header()

    tab_stats, tab_registrar, tab_actualizar, tab_obtener, tab_desactivar, tab_reactivar, tab_eliminar, tab_historial, tab_listado = st.tabs(
        ["📈 Estadísticas", "Registrar", "Actualizar", "Obtener", "Desactivar", "Reactivar", "Eliminar", "Historial", "Ver clientes"]
    )

    with tab_stats:
        render_stats_view()

    with tab_registrar:
        render_register_view()

    with tab_actualizar:
        render_update_view()

    with tab_obtener:
        render_get_view()

    with tab_desactivar:
        render_deactivate_view()

    with tab_reactivar:
        render_reactivate_view()

    with tab_eliminar:
        render_delete_view()

    with tab_historial:
        render_audit_view()

    with tab_listado:
        render_list_view()

    render_footer()


if __name__ == "__main__":
    main()